# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, _, api


def update_data_hooks(cr, registry):
    def set_inactive(rec):
        if rec:
            rec.active = False

    env = api.Environment(cr, SUPERUSER_ID, {})
    # Update value on Company
    env.ref("base.main_company").write(
        {
            # รายได้ค่าปรับ
            "wa_fines_late_account_id": env.ref("egov_coa.1_account_49910003").id,
            "wa_fines_rate": 100,
            "retention_account_id": env.ref("egov_coa.1_account_21030003").id,
            "retention_receivable_account_id": env.ref(
                "egov_coa.1_account_12020002"
            ).id,
            "anglo_saxon_accounting": True,
            "no_space_title_name": True,
            # Tax Thai Format
            "wht_form_preprint": False,
            "tax_report_format": "rd",
            "wht_report_format": "rd",
            # Expense
            "disable_confirm_expense_duplicate": True,
            "asset_move_line_analytic": True,
            "stock_account_line_debit": True,
            "annual_inventory_day": 30,
            "annual_inventory_month": "9",
        }
    )
    # Archive demo data
    set_inactive(env.ref("hr.dep_administration", False))
    set_inactive(env.ref("hr.dep_sales", False))
    set_inactive(env.ref("hr.res_partner_admin_private_address", False))
    set_inactive(env.ref("operating_unit.main_operating_unit", False))
    set_inactive(
        env.ref(
            "purchase_request_tier_validation.purchase_request_default_tier_definition",
            False,
        )
    )
    set_inactive(env.ref("stock.warehouse0", False))
    set_inactive(env.ref("stock.stock_location_stock", False))
    set_inactive(env.ref("stock.picking_type_in", False))
    set_inactive(env.ref("stock.picking_type_out", False))

    # Enable Permission to all users
    # - Work Acceptance, Invoice's Retention
    # - Analytic Account
    env.ref("base.group_user").write(
        {
            "implied_ids": [
                (4, env.ref("purchase_work_acceptance.group_enable_wa_on_po").id),
                (4, env.ref("purchase_work_acceptance.group_enable_wa_on_in").id),
                (4, env.ref("purchase_work_acceptance.group_enforce_wa_on_in").id),
                (
                    4,
                    env.ref("purchase_work_acceptance.group_enable_wa_on_invoice").id,
                ),
                (
                    4,
                    env.ref("purchase_work_acceptance.group_enforce_wa_on_invoice").id,
                ),
                (
                    4,
                    env.ref(
                        "purchase_work_acceptance_evaluation" ".group_enable_eval_on_wa"
                    ).id,
                ),
                (
                    4,
                    env.ref(
                        "purchase_work_acceptance_late_fines"
                        ".group_enable_fines_on_wa"
                    ).id,
                ),
                (
                    4,
                    env.ref(
                        "account_invoice_payment_retention.group_payment_retention"
                    ).id,
                ),
                # Enable Analytic Account
                (
                    4,
                    env.ref("analytic.group_analytic_accounting").id,
                ),
                # Require Analytic
                (
                    4,
                    env.ref("budget_control.group_required_analytic").id,
                ),
                # Multi Route
                (
                    4,
                    env.ref("stock.group_adv_location").id,
                ),
            ]
        }
    )
    # Compute date range
    env["date.range.type"].autogenerate_ranges()

    # Onchange Budget Template Line
    budget_template_lines = env["budget.template.line"].search([])
    for budget_template_line in budget_template_lines:
        budget_template_line._onchange_kpi_id()
        budget_template_line._onchange_account_ids()

    # Onchange Audit Role
    env.ref("egov_user_role.role_audit").onchange_is_readonly_user()

    # Update all tier for check budget
    tier_definition = env["tier.definition"].search([("check_budget", "=", False)])
    tier_definition.write({"check_budget": True})

    # Auto Create Analytic Tag Dimension
    dimensions = env["account.analytic.dimension"].search([])
    for dimension in dimensions:
        dimension.create_analytic_tags()

    # Install th_TH language
    lang_install_wizard = env["base.language.install"].create({"lang": "th_TH"})
    lang_install_wizard.lang_install()

    # Update Date Format
    lang = env["res.lang"].search([("active", "=", True)])
    date_format = "%d/%m/%Y"
    lang.write({"date_format": date_format})

    # Update Guarantee Method Account
    account_21030002 = env.ref("egov_coa.1_account_21030002")
    bid_guarantee = env.ref("l10n_th_gov_purchase_guarantee.bid_guarantee")
    bid_guarantee.account_id = account_21030002
    performance_bond = env.ref("l10n_th_gov_purchase_guarantee.performance_bond")
    performance_bond.account_id = account_21030002
    advance_payment_guarantee = env.ref(
        "l10n_th_gov_purchase_guarantee.advance_payment_guarantee"
    )
    advance_payment_guarantee.account_id = env.ref("egov_coa.1_account_21030001")

    # Update Employee Advance Data
    advance_account = env.ref("egov_coa.1_account_11030001")
    advance_activity = env.ref(
        "budget_activity_advance_clearing.budget_activity_advance"
    )
    advance_activity.account_id = advance_account
    advance_product = env.ref("hr_expense_advance_clearing.product_emp_advance")
    advance_product.property_account_expense_id = advance_account

    # Update Deposit Data
    deposit_account = env.ref("egov_coa.1_account_11060001")
    deposit_activity = env.ref(
        "budget_activity_purchase_deposit.budget_activity_purchase_deposit"
    )
    deposit_activity.account_id = deposit_account
    deposit_product = env.ref(
        "budget_activity_purchase_deposit.product_purchase_deposit"
    )
    deposit_product.property_account_income_id = deposit_account
    deposit_product.property_account_expense_id = deposit_account

    # Update Template KPI (Advance, Deposit) in Budget Template
    kpi_advance = env.ref("budget_activity_advance_clearing.budget_kpi_advance")
    kpi_deposit = env.ref(
        "budget_activity_purchase_deposit.budget_kpi_purchase_deposit"
    )
    env.ref("base.egov_budget_template_01").write(
        {
            "line_ids": [
                (
                    0,
                    0,
                    {
                        "kpi_id": kpi_advance.id,
                        "activity_ids": kpi_advance.activity_ids.ids,
                        "account_ids": kpi_advance.activity_ids.mapped(
                            "account_id"
                        ).ids,
                    },
                ),
                (
                    0,
                    0,
                    {
                        "kpi_id": kpi_deposit.id,
                        "activity_ids": kpi_deposit.activity_ids.ids,
                        "account_ids": kpi_deposit.activity_ids.mapped(
                            "account_id"
                        ).ids,
                    },
                ),
            ]
        }
    )

    # Update Employee Admin
    env.ref("hr.employee_admin").write(
        {
            "address_id": env.ref("base.main_partner").id,
            "address_home_id": env.ref("base.partner_admin").id,
            "default_operating_unit_id": env.ref("base.operating_unit_01").id,
        }
    )

    Journal = env["account.journal"]
    all_journal = Journal.search([], order="id")
    journal_bank = all_journal.filtered(lambda l: l.type == "bank")

    # Check not affect budget on journal
    journal_not_affect_budget = all_journal.filtered(
        lambda l: l.type in ["bank", "cash", "sale"]
        or l.name
        in ["Asset Transfer", "Cash Basis Taxes", "Asset", "Inventory Valuation"]
    )
    journal_not_affect_budget.write({"not_affect_budget": True})

    # Create new reconcile
    env["account.reconcile.model"].sudo().create(
        {
            "name": _("Bank Reconcile Matching Rule"),
            "sequence": "2",
            "rule_type": "invoice_matching",
            "auto_reconcile": False,
            "match_journal_ids": [(6, 0, journal_bank.ids)],
            "match_nature": "both",
            "match_same_currency": True,
            "match_partner": False,
            "match_text_location_label": True,
        }
    )

    # Update sequence date range 20 years
    all_sequence_date_range = env["ir.sequence"].search([("use_date_range", "=", True)])
    date_range = []
    for y in range(2022, 2043):
        date_from = "{}-10-01".format(y)
        date_range.append(
            (0, 0, {"date_from": date_from, "date_to": "{}-09-30".format(y + 1)})
        )
    all_sequence_date_range.write({"date_range_ids": date_range})
