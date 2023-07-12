import xmlrpc.client
import hmac
import hashlib
import logging
import requests
import json
import os

from odoo import http, tools
from odoo.http import request


class APIEndpoint(http.Controller):
    @http.route('/api/v1', auth='none', type='json', methods=['GET', 'POST'], csrf=False)
    def endpoint(self, **kwargs):
        return {'success': 'true', 'message': 'not implemented yet'}
