# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ManagerModel(models.Model):
    _name = "leadquelle.manager.model"
    _description = "Model for manage actions"

    action = fields.Char("Action", required=True)
    label = fields.Char("Label", required=True)
    icon = fields.Char("Icon", required=True)
    access = fields.Selection(
        [("all", "All"), ("admin", "Admin")],
        "Access rights", required=True, default="all")

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """
        Filter records based on user access
        """
        user = self.env.user
        if not user.has_group("base.group_erp_manager"):
            args += [("access", "=", "all")]
        return super(ManagerModel, self).search(args, offset, limit, order, count)

    def execute_action(self):

        self.ensure_one()

        if self.action == "integrate_apis":
            return self.integrate_apis()

        return None

    def integrate_apis(self):
        action = self.env.ref('leadquelle.show_apis_integration').read()[0]
        result = self.env['leadquelle.api.integration'].search([], limit=1)
        if result:
            action['res_id'] = result.id
        return action
