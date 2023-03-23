# Copyright 2022 Ecosoft Co., Ltd (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models


class AssetReportXlsx(models.AbstractModel):
    _inherit = "report.account_asset_management.asset_report_xls"

    def _get_asset_template(self):
        res = super()._get_asset_template()
        res.update(
            {
                "class": {
                    "header": {"type": "string", "value": self._("Asset Class")},
                    "asset": {
                        "type": "string",
                        "value": self._render("asset.class_id.name or ''"),
                    },
                    "width": 30,
                },
            }
        )
        return res
