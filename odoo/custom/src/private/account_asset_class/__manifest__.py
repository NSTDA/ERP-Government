# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Asset Class",
    "version": "15.0.1.0.0",
    "category": "EGOV",
    "license": "AGPL-3",
    "author": "Ecosoft",
    "depends": [
        "account_asset_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_asset_class_views.xml",
        "views/account_asset_views.xml",
    ],
    "installable": True,
    "maintainers": ["ps-tubtim"],
    "development_status": "Alpha",
}
