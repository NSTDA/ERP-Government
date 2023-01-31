# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "EGOV - Excel for Budget Control Sheet",
    "summary": "Import/Export Excel for Budget Control Sheet",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "category": "EGOV",
    "depends": [
        "excel_import_export",
        "budget_control",
    ],
    "external_dependencies": {"python": ["pandas", "numpy", "openpyxl"]},
    "data": [
        "views/actions.xml",
        "templates/templates.xml",
    ],
    "installable": True,
}
