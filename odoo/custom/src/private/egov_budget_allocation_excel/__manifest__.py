# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "EGOV - Excel for Budget Allocation",
    "summary": "Import/Export Excel for Budget Allocation",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": "Ecosoft",
    "category": "EGOV",
    "depends": [
        "excel_import_export",
        "budget_allocation",
    ],
    "external_dependencies": {"python": ["pandas", "numpy", "openpyxl"]},
    "data": [
        "views/actions.xml",
        "templates/templates.xml",
    ],
    "installable": True,
}
