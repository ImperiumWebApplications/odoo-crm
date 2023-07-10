#!/bin/bash

echo "Deploy k8s cluster..."

read -p "Enter the name for this project (will be used as namespace and names for custom k8s resources): " project_name
export CLUSTER_PROJECT_NAME=$project_name

echo "Installing kubelet kubeadm kubectl..."
hostnamectl set-hostname $project_name
apt update
apt upgrade -y
apt install curl gnupg2 apt-transport-https -y
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list
apt update
apt -y install vim git curl wget kubelet kubeadm kubectl

echo "Configuring kubernetes..."
apt-mark hold kubelet kubeadm kubectl
systemctl enable --now kubelet
kubeadm version
swapoff -a

modprobe overlay
modprobe br_netfilter

cat <<EOF | tee /etc/sysctl.d/kubernetes.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sysctl --system

echo "Installing containerd..."
cat <<EOF | tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF

sysctl --system
apt install curl gnupg2 software-properties-common apt-transport-https ca-certificates -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt update
apt install containerd.io -y
mkdir -p /etc/containerd
containerd config default>/etc/containerd/config.toml
systemctl restart containerd
systemctl enable containerd

echo "Deploying kubernetes..."
kubeadm config images pull
kubeadm init --pod-network-cidr=10.244.0.0/16
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

echo "Allowing scheduling of pods on master node..."
kubectl taint node $custom_hostname node-role.kubernetes.io/control-plane:NoSchedule-

echo "Installing helm..."
curl https://baltocdn.com/helm/signing.asc | apt-key add -
apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list
apt-get update
apt-get install helm
helm version

echo "Installing ingress-nginx..."
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace

echo "Installing metallb..."
# see what changes would be made, returns nonzero returncode if different
kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl diff -f - -n kube-system

# actually apply the changes, returns nonzero returncode on errors only
kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl apply -f - -n kube-system

kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml
sleep 15s
read -p "Enter metallb host IP-address: " ip_address
if [[ ! $ip_address =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Wrong format for IP-address!"
    exit 1
fi
export METALLB_HOST=$ip_address
cd kubernetes/metallb
helm package .
envsubst < values.yaml | helm upgrade --install metallb-config ./metallb-config-1.0.0.tgz --values -
cd ../..

echo "Installing local-path-storage..."
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.23/deploy/local-path-storage.yaml

echo "Installing cert-manager..."
helm repo add jetstack https://charts.jetstack.io
helm repo update
kubectl create namespace cert-manager
kubectl apply --validate=false -f https://github.com/cert-manager/cert-manager/releases/download/v1.11.0/cert-manager.crds.yaml
helm install cert-manager jetstack/cert-manager --namespace cert-manager --version v1.11.0 --set webhook.hostNetwork=true,webhook.securePort=10260

echo "K8s cluster deployed"