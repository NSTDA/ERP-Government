# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

import base64
import math
from io import BytesIO

import pandas as pd
from dateutil.relativedelta import relativedelta
from openpyxl.utils.dataframe import dataframe_to_rows

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class XLSXImport(models.AbstractModel):
    _inherit = "xlsx.import"

    @api.model
    def import_xlsx(self, import_file, template, res_model=False, res_id=False):
        if self._context.get("is_budget_control_sheet"):
            import_file = self.sudo()._transform_budget_control_sheet(import_file)
        record = super().import_xlsx(
            import_file, template, res_model=res_model, res_id=res_id
        )
        return record

    def _get_lock_date(self, lock_amount):
        date = fields.Date.context_today(self)
        if lock_amount == "last":
            date = date.replace(day=1) - relativedelta(days=1)
        elif lock_amount == "current":
            date += relativedelta(day=31)  # change to last month
        return date

    def _get_matrix_from_excel(self, import_file):
        content = BytesIO(base64.decodebytes(import_file))
        df = pd.read_excel(content, sheet_name="BudgetControl", header=None)
        matrix_df = df.iloc[8:, :14]  # Get only matrix from cell A9 to column N
        return matrix_df

    def _create_df_import_data(self, budget_items):
        result_df = pd.DataFrame(budget_items)
        # Ensure amount is summed for the same keys
        result_df = result_df.groupby([0, 1, 2, 3, 4, 6])[[5]].sum()
        result_df = result_df.reset_index().sort_index(axis=1)
        return result_df

    def _transform_budget_control_sheet(self, import_file):
        """Convert worksheet 'BudgetControl' to 'ImportData' and import by line"""
        lock_amount = self.env.company.budget_control_revision_lock_amount
        lock_date = self._get_lock_date(lock_amount)

        budget_control = self.env["budget.control"].browse(self._context["active_id"])

        # Read excel from sheet "BudgetControl" as data frame
        matrix_df = self._get_matrix_from_excel(import_file)

        # Expand the matrix into budget.control.line table
        # [budget_control, kpi, date_range, date_from, date_to, amount, analytic]
        rows = dataframe_to_rows(matrix_df, index=False, header=False)
        # Filter excel column A (KPI) is not null
        rows = [
            x
            for x in rows
            if x != [0] and not (isinstance(x[0], float) and math.isnan(x[0]))
        ]

        # Check if there are 12 periods for budget control
        periods = self.env["date.range"].search(
            [
                ("date_start", ">=", budget_control.date_from),
                ("date_end", "<=", budget_control.date_to),
                ("type_id", "=", budget_control.plan_date_range_type_id.id),
            ],
            order="date_start",
        )
        if len(periods) != 12:
            raise ValidationError(_("Cannot setup 12 periods for budget control"))

        budget_items = []
        line_ids = budget_control.line_ids
        # Clear old template lines
        budget_control.template_line_ids = False
        template_lines = budget_control.template_id.line_ids
        template_line_ids = []
        budget_control_id = self.get_external_id(budget_control)
        analytic_id = self.get_external_id(budget_control.analytic_account_id)

        for r in rows:
            kpi = r[0]
            # Find line amount check not edit past amount.
            lines = line_ids.filtered(lambda l: l.name == kpi)
            row_amount = []
            # Get template line, KPI will compute following template line
            template_line = template_lines.filtered(lambda l: l.name == kpi)
            template_line_ids.append(template_line.id)
            template_line_id = (
                self.get_external_id(template_line) if template_line else ""
            )

            for m in range(0, 12):
                if lock_amount != "none" and not budget_control.init_revision:
                    period_end = periods[m].date_end
                    # lock amount
                    if period_end <= lock_date:
                        amount = float(r[m + 1])
                        # Convert Nan -> 0.0
                        if math.isnan(amount):
                            amount = 0.0
                        row_amount.append(amount)
                budget_items.append(
                    [
                        budget_control_id,  # Budget Control
                        template_line_id,  # Template Line
                        periods[m].name,  # Date Range
                        periods[m].date_start,  # From
                        periods[m].date_end,  # To
                        r[m + 1],  # Amount
                        analytic_id,  # Analytic
                    ]
                )
            # Not allow edit past amount,
            # - No lines in budget control but add amount in excel
            # - There are lines in budget control and edit past amount in excel
            if not lines and any(x != 0.0 for x in row_amount):
                raise ValidationError(_("Cannot edit past amount."))
            elif (
                lines
                and lines.filtered(lambda l: l.is_readonly).mapped("amount")
                != row_amount
            ):
                raise ValidationError(_("Cannot edit past amount."))

        # Add New Plan
        budget_control.template_line_ids = [(6, 0, template_line_ids)]

        # Create data frame from budget.control.line data table, and return as new excel
        result_df = self._create_df_import_data(budget_items)
        new_content = BytesIO()
        result_df.to_excel(
            new_content, sheet_name="ImportData", index=False, header=False
        )
        new_content.seek(0)  # Set index to 0, and start reading
        new_file = base64.encodebytes(new_content.read())
        return new_file
