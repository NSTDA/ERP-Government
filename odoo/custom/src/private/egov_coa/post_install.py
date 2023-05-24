# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def post_init_hook(cr, registry):
    from odoo.addons.account.models.chart_template import (
        preserve_existing_tags_on_taxes,
    )

    preserve_existing_tags_on_taxes(cr, registry, "egov_coa")
