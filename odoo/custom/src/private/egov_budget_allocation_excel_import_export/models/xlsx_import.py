# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models
from odoo.exceptions import UserError


class XLSXImport(models.AbstractModel):
    _inherit = "xlsx.import"

    @api.model
    def _get_line_vals(self, st, worksheet, model, line_field):
        vals = super()._get_line_vals(st, worksheet, model, line_field)
        Analytic = self.env["account.analytic.account"]
        # Convert analytic account name to id database because
        # it can full name is "[code] year: name - customer"
        analytic_account = vals.get("line_ids/analytic_account_id/.id", [])
        for idx, aa in enumerate(analytic_account):
            aa_split = aa.split(":")
            if len(aa_split) == 1:
                raise UserError(_("Format analytic account is not correct."))
            # Split the fullname part into period and fullname"
            aa_period = aa_split[0].strip()
            aa_fullname = aa_split[1].strip()
            # Check the fullname part, i.e., "name - customer", Get name only
            aa_name = aa_fullname.split(" - ")[0].strip()
            analytic = Analytic.search([("name", "=", aa_name)])
            if len(analytic) > 1 and aa_period:
                # Check the code part, i.e., "[CODE1] 2022", Get year only
                if aa_period.rfind("[") >= 0:
                    aa_period = aa_period[aa_period.rfind(" ") :].strip()
                analytic = analytic.filtered(
                    lambda l: l.budget_period_id.name == aa_period
                )
            analytic_account[idx] = analytic.id
        return vals
