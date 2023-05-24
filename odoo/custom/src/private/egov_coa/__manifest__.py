# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "eGov - Accounting",
    "version": "15.0.1.0.0",
    "category": "Accounting & Finance",
    "summary": "Chart of Accounts for eGov.",
    "author": "Ecosoft",
    "website": "http://ecosoft.co.th/",
    "depends": ["account"],
    "license": "AGPL-3",
    "data": [
        "data/egov_chart_data.xml",
        "data/account.chart.template.csv",
        "data/account.account.template.csv",
        "data/egov_chart_post_data.xml",
        "data/account_tax_template_data.xml",
        "data/account_chart_template_data.xml",
    ],
    "post_init_hook": "post_init_hook",
}
