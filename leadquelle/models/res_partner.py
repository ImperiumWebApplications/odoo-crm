from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    custom_field_1 = fields.Char(string="Custom Field 1")
    custom_field_2 = fields.Integer(string="Custom Field 2")
