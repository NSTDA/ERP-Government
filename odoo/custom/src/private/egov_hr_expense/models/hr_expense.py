# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrExpense(models.Model):
    _inherit = "hr.expense"

    product_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "reported": [("readonly", False)],
            "refused": [("readonly", False)],
        },
    )
    clearing_product_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "reported": [("readonly", False)],
            "refused": [("readonly", False)],
        },
    )

    @api.model
    def _get_under_validation_exceptions(self):
        res = super()._get_under_validation_exceptions()
        res.extend(["date_commit"])
        return res


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    name = fields.Char(
        states={"done": [("readonly", True)], "post": [("readonly", True)]},
    )

    def action_submit_sheet(self):
        res = super().action_submit_sheet()
        # Request Validation after Submit to Manager
        if self.need_validation:
            self.request_validation()
        return res

    def refuse_sheet(self, reason):
        """Allow refuse with state draft, no permission"""
        # Accountant and User in tier validation can refuse expense state submit, approved
        if (
            not self.env.user.has_group("account.group_account_invoice")
            and self.filtered(lambda l: l.state in ["submit", "appove"])
            and not self._context.get("default_validate_reject")
        ):
            raise UserError(_("Only Accountant can refuse expenses."))
        # Employee can refuse expense state draft only
        if self._context.get("self_refuse", False):
            self.write({"state": "cancel"})
            for sheet in self:
                sheet.message_post_with_view(
                    "hr_expense.hr_expense_template_refuse_reason",
                    values={"reason": reason, "is_sheet": True, "name": sheet.name},
                )
            return self.activity_update()
        return super().refuse_sheet(reason)
