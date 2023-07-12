import xmlrpc.client
import hmac
import hashlib
import json
import os

from odoo import http, tools
from odoo.http import request


def validate_signature(checking_request, secret_key):
    signature = checking_request.headers.get('X-Hub-Signature')
    if not signature:
        return False
    sha_name, signature = signature.split('=')
    if sha_name != 'sha1':
        return False
    mac = hmac.new(bytes(secret_key, 'latin1'), msg=checking_request.get_data(), digestmod=hashlib.sha1)
    print(str(mac.hexdigest()))
    return hmac.compare_digest(str(mac.hexdigest()), str(signature))


def get_api_integration():
    success, message = True, "Ok"

    host = tools.config['http_interface']
    host = host if host else 'localhost'
    port = tools.config['http_port']
    db = tools.config['db_name']
    username = os.environ.get('ODOO_ADMIN_USERNAME')
    if not username:
        username = 'admin'
    password = os.environ.get('ODOO_ADMIN_PASSWORD')
    if not password:
        password = tools.config['admin_passwd']
    url = f'http://{host}:{port}/xmlrpc/2'

    uid = xmlrpc.client.ServerProxy(f'{url}/common').authenticate(db, username, password, {})

    if uid > 0:
        models = xmlrpc.client.ServerProxy(f'{url}/object')
        integration = models.execute_kw(
            db, uid, password, 'leadquelle.api.integration', 'search_read', [[]],
            {'fields': ['user_login', 'thirdparty_integration_api_key'], 'limit': 1})
        if integration:
            success, message = True, integration[0]
        else:
            success, message = False, "There are no integration for API"
    else:
        success, message = False, "Unauthorized (admin)"

    return success, message


class APIEndpoint(http.Controller):
    @http.route('/api/v1', auth='none', type='json', methods=['GET', 'POST'], csrf=False)
    def endpoint(self, **kwargs):
        success, message = get_api_integration()

        if success:
            integration = message
            if validate_signature(request.httprequest, integration['thirdparty_integration_api_key']):

                success, message = True, 'Not implemented yet'
            else:
                success, message = False, "Unauthorized (signature)"

        return {'success': success, 'message': message}
