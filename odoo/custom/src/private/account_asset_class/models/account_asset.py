# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountAsset(models.Model):
    _inherit = "account.asset"

    class_id = fields.Many2one(
        comodel_name="account.asset.class",
        string="Asset Class",
        domain="[('asset_profile_id', '=', profile_id)]",
        ondelete="cascade",
        tracking=True,
        check_company=True,
    )

    @api.model
    def _xls_acquisition_fields(self):
        res = super()._xls_acquisition_fields()
        return res + ["class"]

    @api.model
    def _xls_active_fields(self):
        res = super()._xls_active_fields()
        return res + ["class"]

    @api.model
    def _xls_removal_fields(self):
        res = super()._xls_removal_fields()
        return res + ["class"]
