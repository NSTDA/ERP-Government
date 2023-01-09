# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"
    _state_from = ["to_approve"]  # Change state from - to for tier validation
    _state_to = ["approved"]

    def request_validation(self):
        # Only verified document can start tier
        for rec in self.filtered("substate_id"):
            if rec.substate_id.sequence != 20:
                raise UserError(_("Document is not verified!"))
        return super().request_validation()

    @api.model
    def _get_under_validation_exceptions(self):
        res = super()._get_under_validation_exceptions()
        res.extend(["state", "substate_id", "approved_by", "date_approved"])
        return res
