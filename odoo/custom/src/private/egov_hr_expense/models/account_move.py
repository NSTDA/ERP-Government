# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def js_remove_outstanding_partial(self, partial_id):
        """Auto cancel payment related expense"""
        res = super().js_remove_outstanding_partial(partial_id)
        self.ensure_one()
        if self.payment_id.expense_sheet_ids:
            self.payment_id.action_draft()
            self.payment_id.action_cancel()
        return res
