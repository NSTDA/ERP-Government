# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAssetLine(models.Model):
    _inherit = "account.asset.line"

    type = fields.Selection(readonly=False)
    line_days = fields.Integer(readonly=False)
