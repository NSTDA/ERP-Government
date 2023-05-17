# Copyright 2022 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import http
from odoo.http import request


class WebhookController(http.Controller):
    @http.route("/create_pr", type="json", auth="user")
    def create_pr_data(self, model, vals):
        pr_rule = request.env["exception.rule"].search(
            [("model", "=", "purchase.request")]
        )
        pr_rule.write({"active": False})
        pr_tier = request.env["tier.definition"].search(
            [("model", "=", "purchase.request")]
        )
        pr_tier.write({"active": False})
        model_id = request.env[model].create(vals)
        model_id.button_to_approve()
        model_id.with_context(to_substate_sequence=20).action_to_substate()
        model_id.button_approved()
        return model_id

    @http.route("/create_ex", type="json", auth="user")
    def create_ex_data(self, model, vals):
        ex_tier = request.env["tier.definition"].search(
            [("model", "=", "hr.expense.sheet")]
        )
        ex_tier.write({"active": False})
        model_id = request.env[model].create(vals)
        model_id.action_submit_sheet()
        model_id.approve_expense_sheets()
        model_id.action_sheet_move_create()
        return model_id
