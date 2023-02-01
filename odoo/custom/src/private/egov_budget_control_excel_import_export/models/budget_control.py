# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class BudgetControl(models.Model):
    _inherit = "budget.control"

    template_line_all = fields.One2many(
        comodel_name="budget.template.line",
        related="template_id.line_ids",
        help="Used to povide list of KPIs (Template lines) in excel sheet",
    )
