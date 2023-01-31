# Copyright 2022 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

import base64
import math
from io import BytesIO

import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows

from odoo import _, api, models
from odoo.exceptions import ValidationError


class XLSXImport(models.AbstractModel):
    _inherit = "xlsx.import"

    @api.model
    def import_xlsx(self, import_file, template, res_model=False, res_id=False):
        if self._context.get("is_budget_control_sheet"):
            import_file = self._transform_budget_control_sheet(import_file)
        record = super().import_xlsx(
            import_file, template, res_model=res_model, res_id=res_id
        )
        return record

    def _transform_budget_control_sheet(self, import_file):
        MISReportKPI = self.env["mis.report.kpi"]
        MISKPIExpression = self.env["mis.report.kpi.expression"]
        # Get the budget control sheet
        res_id = self._context["active_id"]
        budget_control = self.env["budget.control"].browse(res_id)
        analytic_id = budget_control.analytic_account_id
        budget_id = budget_control.budget_id
        # Read excel from sheet "BudgetControl" as data frame
        content = BytesIO(base64.decodebytes(import_file))
        df = pd.read_excel(content, sheet_name="BudgetControl", header=None)
        matrix_df = df.iloc[8:, :14]  # Get only matrix from cell A9 to column N
        # Expand the matrix into mis.budget.item table
        # [kpi, period, amount, budget_id, date_from, date_to, anlaytic]
        rows = dataframe_to_rows(matrix_df, index=False, header=False)
        # Filter excel column A (AG) is not null
        rows = [
            x
            for x in rows
            if x != [0] and not (isinstance(x[0], float) and math.isnan(x[0]))
        ]
        periods = self.env["date.range"].search(
            [
                ("date_start", ">=", budget_control.date_from),
                ("date_end", "<=", budget_control.date_to),
                ("type_id", "=", self.env.ref("base.date_range_type_period").id),
            ],
            order="date_start",
        )
        if len(periods) != 12:
            raise ValidationError(_("Cannot setup 12 periods for budget control"))
        budget_items = []
        item_ids = budget_control.item_ids
        # Clear Old AG
        budget_control.kpi_ids = False
        kpi_ids = []
        for r in rows:
            kpi = r[0]
            ag = kpi.strip()
            # Get the description part, i.e., "AG1 (ag1)" -> "AG1"
            if ag.endswith(")") and "(" in ag:
                ag = ag[: ag.rfind("(")].strip()
            # Find line amount check not edit past amount.
            item = item_ids.filtered(lambda l: l.name == kpi)
            row_amount = []
            kpi_id = MISReportKPI.search(
                [
                    ("description", "=", ag),
                    ("report_id", "=", budget_control.budget_id.report_id.id),
                ],
                limit=1,
            )
            kpi_expression_id = MISKPIExpression.search([("kpi_id", "=", kpi_id.id)])
            kpi_ids.append(kpi_id.id)
            activity_group_id = kpi_id.activity_group_id
            activity_group = kpi_id and self.get_external_id(activity_group_id) or ""
            for m in range(0, 12):
                if item and item[m].is_readonly:
                    row_amount.append(float(r[m + 1]))
                budget_items.append(
                    [
                        activity_group,  # activity group
                        self.get_external_id(kpi_expression_id),  # KPI
                        periods[m].name,
                        r[m + 1],
                        self.get_external_id(budget_id),
                        periods[m].date_start,
                        periods[m].date_end,
                        self.get_external_id(analytic_id),
                    ]
                )
            if item.filtered(lambda l: l.is_readonly).mapped("amount") != row_amount:
                raise ValidationError(_("Cannot edit past amount."))

        # Add New Plan
        budget_control.kpi_ids = [(6, 0, kpi_ids)]
        # Create data frame from mis.budget.item data table, and return as new excel
        result_df = pd.DataFrame(budget_items)
        # Ensure amount is summed for the same keys
        result_df = result_df.groupby([0, 1, 2, 4, 5, 6, 7])[[3]].sum()
        result_df = result_df.reset_index().sort_index(axis=1)
        new_content = BytesIO()
        result_df.to_excel(
            new_content, sheet_name="ImportData", index=False, header=False
        )
        new_content.seek(0)  # Set index to 0, and start reading
        new_file = base64.encodebytes(new_content.read())
        return new_file
