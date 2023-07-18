# -*- coding: utf-8 -*-
# from odoo import http


# class ContactsImport(http.Controller):
#     @http.route('/contacts_import/contacts_import', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contacts_import/contacts_import/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('contacts_import.listing', {
#             'root': '/contacts_import/contacts_import',
#             'objects': http.request.env['contacts_import.contacts_import'].search([]),
#         })

#     @http.route('/contacts_import/contacts_import/objects/<model("contacts_import.contacts_import"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contacts_import.object', {
#             'object': obj
#         })
