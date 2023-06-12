# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "EGOV - Master Data and Configuration",
    "summary": "Used to import data and config",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "category": "EGOV",
    "author": "Ecosoft",
    "installable": True,
    "depends": [
        "egov_install",
        "egov_coa",
    ],
    "data": [
        "data/account_account_data.xml",
        "data/operating.unit.csv",
        "data/res.users.csv",
        "data/res_company_data.xml",
        "data/stock.warehouse.csv",
        "data/hr.department.csv",
        "data/hr.employee.csv",
        "data/account.journal.csv",
        "data/account.withholding.tax.csv",
        "data/budget.kpi.csv",
        "data/budget.activity.csv",
        "data/date.range.type.csv",
        "data/res_partner_data.xml",
        "data/hr_department_data.xml",
        "data/budget.template.csv",
        "data/tier_reviewer_extra_access.xml",
        "data/ir_model_access_data.xml",
    ],
    "post_init_hook": "update_data_hooks",
}
