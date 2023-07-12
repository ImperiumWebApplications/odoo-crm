# -*- coding: utf-8 -*-
from odoo import fields, models, api


class APIsIntegration(models.Model):
    _name = "leadquelle.api.integration"
    _description = "Model for integrations"

    user_id = fields.Many2one("res.users", string="User for integration", required=True)
    thirdparty_integration_api_key = fields.Char("Odoo API Key", required=True,
                                                 help="Create Leadquelle API key for use in third party services")

    user_login = fields.Char("Login for virtual user for integrations", compute="_compute_user_login")

    @api.depends("user_id")
    def _compute_user_login(self):
        for record in self:
            record.user_login = record.user_id.login

    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = f"APIs integration"
            result.append((record.id, name))
        return result
