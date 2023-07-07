# FonFon Odoo

## Deploy kubernetes

### For dev environment:
1. Copy `kubernetes` folder to the kubernetes dev server
2. Update permissions: `chmod u+r+x kubernetes/deploy_k8s_dev.sh`
3. Run `./kubernetes/deploy_k8s_dev.sh` script under `root`

After kubernetes cluster have deployed and configured you should create Kubernetes integration using GitLab CI/CD

##### GitLab CI/CD Kubernetes integration
1. In the GitLab project go to **Infrastructure > Kubernetes clusters**;
2. Select **Connect a cluster (agent)**;
3. Type a name which you want for your agent;
4. Select **Register an agent**;
5. Run command shown by GitLab in your k8s cluster.
6. Go to **Settings > CI/CD > Variables**
7. Add variable `DOCKERFILE_PATH` with value `docker/Dockerfile`

*More details: https://docs.gitlab.com/ee/user/clusters/agent/install/index.html#register-the-agent-with-gitlab*

From now CI/CD is ready, check `.gitlab-ci.yml` for configuration.

##### Zammad deployment
Zammad can be deployed under kubernetes via Helm: 
```
# Add Helm repo
$ helm repo add zammad https://zammad.github.io/zammad-helm

# Install / Upgrade Zammad
$ helm upgrade --install zammad zammad/zammad --namespace=zammad
```

Dev configuration of the k8s use host-path storage class, so then you need to update all Persistent Volume Claims for 
`zammad` namespace by adding or editing field `spec -> storageClassName` - just set value `storageClassName: local-path`

Also, you need to apply manifest from `kubernetes -> zammad -> zammad-ingress.yaml` to open service to the world. 
You can edit public url in the `zammad-ingress.yaml` manifest under `spec -> rules -> host` field. 

##### Asterisk deployment

Asterisk server wih freepbx deploy to kubernetes from FonFon repository. Also FonFon use odoo’s module Asterisk plus for 
integration odoo with Asterisk server. 

After deploy:

1. Make sure that base url is under ***https***: go to `Settigs -> Technical -> System Parameters -> web.base.url` and check the URL.
2. Go to FreePBX admin page for asterisk server (f. e. `pbx.fonfonllc.com`),
    a. Go to `Settings -> Asterisk Manager Users` and add new manager user, f.e. 
    ```
    username: odoo
    password: odoo_pass
    deny=0.0.0.0/0.0.0.0
    permit=10.244.0.1/255.255.255.0
    ```
    Where `permit=10.244.0.1/255.255.255.0` is kubernetes internal IPs of your services. And don’t forget to click `Apply Config` button.
3. Go to Asterisk Plus module in odoo: `PBX -> Settings -> Server`
    a. Fill `AMI User` and `AMI Password` fields with creds from previous step;
    b. Fill `AMI Host` with your cluster public IP or hostname;
    c. Fill `AMI Port` with `5038`;
    d. Fill `Built-in HTTP URL` with FreePBX admin page (f. e. `pbx.fonfonllc.com`)
    e. Click `Update` button;
    f. Check integration by clicking `Ping Agent` and `Ping Asterisk` buttons.


## APIs integration
FonFon module has several integrations with 3rd party APIs. For this purpose admin user (and ony admin) should save API 
keys for that integrations. It can be done under `FonFon Module -> Manage FonFon -> Integrations with APIs` menu. 

### Odoo out integration
For some APIs there are need to have access to Odoo modules. For that purpose admin need to create special virtual user, 
then under menu `User -> Preferences -> Account Security -> new API key`. Then in the `Odoo out integration` tab choose 
created virtual user and save the key. 

### Zammad
First, admin shell to add a FonFon webhook to the Zammad.
Usually it can be got under `Manage -> Webhook -> New webhook` menu. In the popup admin shell to fill `endpoint` 
field with `<host>/webhook/zammad` and `HMAC SHA1 signature` with API key from `Odoo out integration` tab.

Then, API key for Zammad integration should be got from Zammad service and save under `Zammad` tab. Zammad API key 
can be got under `User -> Preferences -> Key access -> Create`. Key should be created for admin or special virtual user 
with `ticket.agent` access rights. Key from popup should be saved under `Zammad` tab at FonFon module.

### Mindee
Mindee integration is simple. API key for Mindee should be got from Mindee service under `User -> Settings -> API keys -> Create a new API key`.
Then just save the key under `Mindee` tab at the FonFon module.

### Dialfire
Again, API key for Dialfire integration should be got from Dialfire service under `Prefereces` menu. First admin should get 
a tenant id under `Tenant` menu. Then go to `API Tokens` and create new token for resource: choose the resource, 
add to `Path` string `/api/tenants/<tenant id>` with tenant id from previous step. After token creation save tenant id 
and token under `Dialfire` tab at FonFon module.


