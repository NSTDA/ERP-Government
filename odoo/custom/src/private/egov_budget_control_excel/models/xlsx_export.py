# Copyright 2022 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows

from odoo import api, fields, models


class XLSXExport(models.AbstractModel):
    _inherit = "xlsx.export"

    @api.model
    def _fill_workbook_data(self, workbook, record, data_dict):
        """Fill data processed from pandas after normal fill"""
        all_ou = self.env.user.has_group(
            "budget_control_operating_unit_access_all.group_all_ou_budget_control"
        )
        if all_ou:
            record = record.sudo()
        res = super()._fill_workbook_data(workbook, record, data_dict)
        if self._context.get("is_budget_control_sheet"):
            self._fill_budget_control_sheet(workbook, record)
        return res

    def _get_items_readonly(self, record, date=False):
        if not date:
            date = fields.Date.context_today(self)
        # change current month to previous month
        budget_control_revision_lock_amount = (
            self.env.company.budget_control_plan_readonly
        )
        if budget_control_revision_lock_amount == "last":
            date = date.replace(day=1) - relativedelta(days=1)
        bc_date_from = record.date_from
        daterange_from = {}
        for index in range(2, 14):
            date_from = bc_date_from + relativedelta(months=index - 2)
            if date_from <= date:
                daterange_from[index] = date_from
        return daterange_from

    @api.model
    def _fill_budget_control_sheet(self, workbook, record, date=False):
        if record.item_ids:
            raw_data = workbook["RawData"]
            budget_control = workbook["BudgetControl"]
            df = pd.DataFrame(raw_data.values)
            pd.set_option("display.max_rows", None, "display.max_columns", None)
            # Make pivot_table
            table = pd.pivot_table(
                df,
                values=2,
                index=[0],
                columns=[1],
                aggfunc=np.sum,
                fill_value=0,
                sort=False,
            )
            pos = (1, 9)  # Will paste the pivot table to cell A9
            rows = dataframe_to_rows(table.reset_index(), index=False, header=False)
            # find column readonly on budget control
            daterange_from = self._get_items_readonly(record, date)
            for r_idx, row in enumerate(rows, pos[1]):
                for c_idx, value in enumerate(row, pos[0]):
                    budget_cell = budget_control.cell(
                        row=r_idx, column=c_idx, value=value
                    )
                    if daterange_from.get(c_idx, False):  # Add color amount readonly
                        budget_cell.font = Font(size=10, color="FF0000")
