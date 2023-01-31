# Copyright 2022 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class BudgetControl(models.Model):
    _inherit = "budget.control"

    kpi_all = fields.One2many(
        comodel_name="mis.report.kpi",
        related="budget_id.report_id.kpi_ids",
        help="Used to provide a list of KPIs in an excel sheet",
    )
    activity_all = fields.One2many(
        comodel_name="budget.activity",
        compute="_compute_all_data",
        help="Used to provide a list of activities in an excel sheet",
    )

    def _compute_all_data(self):
        activity_all = self.env["budget.activity"].search([])
        for rec in self:
            rec.activity_all = activity_all
