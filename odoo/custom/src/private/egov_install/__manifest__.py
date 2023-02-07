# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "EGOV - Install",
    "summary": "Used to install other modules",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "category": "EGOV",
    "author": "Ecosoft",
    "installable": True,
    "depends": [
        # Structure
        "account_asset_operating_unit",
        "account_asset_operating_unit_access_all",
        "account_financial_report_operating_unit",
        "account_operating_unit",
        "account_operating_unit_access_all",
        # "account_payment_multi_deduction_operating_unit",
        # "agreement_operating_unit",
        # "agreement_operating_unit_access_all",
        "analytic_operating_unit",
        "analytic_operating_unit_access_all",
        "base_user_role",
        "budget_allocation_operating_unit",
        "budget_allocation_operating_unit_access_all",
        "budget_control_operating_unit",
        "budget_control_operating_unit_access_all",
        "contract_operating_unit",
        "contract_operating_unit_access_all",
        "hr_expense_operating_unit",
        "hr_expense_operating_unit_access_all",
        "hr_operating_unit",
        "hr_operating_unit_access_all",
        "mis_builder_operating_unit",
        # "mis_builder_operating_unit_access_all",
        "operating_unit",
        "operating_unit_access_all",
        "purchase_deposit_operating_unit",
        "purchase_operating_unit",
        "purchase_operating_unit_access_all",
        "purchase_request_operating_unit",
        "purchase_request_operating_unit_access_all",
        "purchase_request_to_requisition_operating_unit",
        "purchase_requisition_operating_unit",
        "purchase_requisition_operating_unit_access_all",
        # "purchase_work_acceptance_late_fines_operating_unit",
        "sale_operating_unit",
        # "sale_operating_unit_access_all",
        "sale_stock_operating_unit",
        "sales_team_operating_unit",
        "stock_operating_unit",
        "stock_operating_unit_access_all",
        # Budgeting
        # "account_asset_transfer_allocation_dimension",
        # "account_asset_transfer_fund",
        # "account_asset_transfer_operating_unit",
        # "account_invoice_payment_retention_budget",
        # "account_invoice_payment_retention_fund",
        # "account_payment_multi_deduction_activity",
        # "account_payment_multi_deduction_dimension",
        # "account_payment_multi_deduction_fund",
        # "base_budget_account_payment_multi_deduction",
        "base_tier_validation_check_budget",
        "budget_activity",
        "budget_activity_advance_clearing",
        "budget_activity_contract",
        "budget_activity_expense",
        "budget_activity_purchase",
        "budget_activity_purchase_request",
        "budget_activity_purchase_requisition",
        "budget_allocation",
        "budget_allocation_advance_clearing",
        "budget_allocation_contract",
        "budget_allocation_department",
        "budget_allocation_expense",
        "budget_allocation_purchase",
        "budget_allocation_purchase_request",
        "budget_allocation_revision",
        "budget_control",
        "budget_control_advance_clearing",
        "budget_control_contract",
        "budget_control_expense",
        "budget_control_purchase",
        "budget_control_purchase_request",
        "budget_control_purchase_requisition",
        "budget_control_revision",
        "budget_control_revision_lock_amount",
        "budget_plan",
        "budget_plan_revision",
        "budget_res_project_department",
        "mis_builder",
        "res_project",
        "res_project_sequence",
        # Procurement
        "l10n_th_gov_purchase_agreement",
        "l10n_th_gov_purchase_request",
        "l10n_th_gov_purchase_guarantee",
        "l10n_th_gov_work_acceptance",
        "purchase_deposit",
        "purchase_invoice_plan",
        # "purchase_invoice_plan_deposit",
        "purchase_invoice_plan_retention",
        "purchase_request",
        "purchase_request_tier_validation",
        "purchase_tier_validation",
        "purchase_work_acceptance",
        "purchase_work_acceptance_evaluation",
        "purchase_work_acceptance_invoice_plan",
        "purchase_work_acceptance_late_fines",
        "purchase_work_acceptance_tier_validation",
        # "purchase_work_acceptance_late_fines_budget",
        # "purchase_work_acceptance_late_fines_fund",
        # Accounting
        "account_financial_report",
        # "account_financial_report_extension",
        "account_lock_date_update",
        "account_payment_multi_deduction",
        "account_reconciliation_widget",
        # "account_spread_cost_revenue",
        # "account_spread_cost_revenue_enhanced",
        "account_statement_import_txt_xlsx",
        "account_usability",
        "hr_expense_advance_clearing",
        "hr_expense_advance_clearing_sequence",
        "hr_expense_cancel",
        "hr_expense_exception",
        "hr_expense_pay_to_vendor",
        "hr_expense_payment",
        "hr_expense_payment_widget_amount",
        "hr_expense_sequence",
        "hr_expense_tier_validation",
        "l10n_th_account_tax",
        "l10n_th_account_tax_expense",
        "l10n_th_account_tax_multi",
        "l10n_th_account_tax_report",
        "l10n_th_account_wht_cert_form",
        "l10n_th_bank_payment_export",
        # "l10n_th_bank_payment_export_bbl",
        "l10n_th_bank_payment_export_ktb",
        "l10n_th_gov_hr_expense",
        "partner_bank_code",
        "sale_invoice_plan",
        "sale_invoice_plan_retention",
        "sale_management",
        # Agreement & Contract
        "agreement",
        "agreement_legal",
        # "agreement_legal_contract",
        "contract",
        # "contract_invoice_plan",
        # "contract_invoice_plan_selection",
        # Asset
        # "account_asset_compute_batch",
        # "account_asset_compute_batch_job",
        # "account_asset_from_expense",
        "account_asset_low_value",
        "account_asset_management",
        "account_asset_transfer",
        "l10n_th_account_asset_management",
        "l10n_th_gov_account_asset_management",
        # Inventory
        "stock_card_report",
        "stock_no_negative",
        "stock_request",
        "stock_request_separate_pickings",
        # Optional
        "egov_hr_expense",
        "egov_purchase",
        "egov_purchase_request",
    ],
}
