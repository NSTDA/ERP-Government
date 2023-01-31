# Copyright 2022 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models
from odoo.exceptions import UserError


class XLSXImport(models.AbstractModel):
    _inherit = "xlsx.import"

    @api.model
    def _get_line_vals(self, st, worksheet, model, line_field):
        vals = super()._get_line_vals(st, worksheet, model, line_field)
        Analytic = self.env["account.analytic.account"]
        # convert analytic account name to id database
        analytic_account = vals.get("allocation_line_ids/analytic_account_id/.id", [])
        aa_format_incorrect = []
        for idx, aa in enumerate(analytic_account):
            aa_split = aa.split(":")
            if len(aa_split) == 1:
                aa_format_incorrect.append(aa_split[0])
            else:
                # Name analytic has special character (:)
                if len(aa_split) > 2:
                    extend_name = ":".join(aa_split[2:])
                    aa_name = ":".join([aa_split[1], extend_name]).strip()
                else:
                    aa_name = aa_split[1].strip()
                aa_period = aa_split[0].strip()
                analytic = Analytic.search([("name", "=", aa_name)])
                if len(analytic) > 1 and aa_period:
                    # Check the code part, i.e., "[CODE1] 2022", Get year only
                    if aa_period.rfind("[") >= 0:
                        aa_period = aa_period[aa_period.rfind(" ") :].strip()
                    analytic = analytic.filtered(
                        lambda l: l.budget_period_id.name == aa_period
                    )
                analytic_account[idx] = analytic.id
        if aa_format_incorrect:
            aa_incorrect_names = "\n".join(aa_format_incorrect)
            raise UserError(
                _("The following analytic accounts are incorrect format:\n{}").format(
                    aa_incorrect_names
                )
            )
        return vals
