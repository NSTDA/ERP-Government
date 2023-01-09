# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "EGOV - Purchase Request",
    "version": "15.0.1.0.0",
    "author": "Ecosoft",
    "category": "EGOV",
    "license": "AGPL-3",
    "depends": [
        "base_tier_validation_server_action",
        "l10n_th_gov_purchase_request",
        "purchase_request_tier_validation",
    ],
    "data": [
        "data/ir_actions_server.xml",
        "views/purchase_request_view.xml",
    ],
    "installable": True,
}
