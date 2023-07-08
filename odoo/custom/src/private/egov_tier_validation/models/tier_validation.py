# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models


class TierValidation(models.AbstractModel):
    _inherit = "tier.validation"

    def _compute_next_review(self):
        """Overwrite function _compute_next_review in 'base_tier_validation'
        for delete word 'Next: <review name>' to '<review name>'"""
        for rec in self:
            review = rec.review_ids.sorted("sequence").filtered(
                lambda l: l.status == "pending"
            )[:1]
            rec.next_review = review and _("%s") % review.name or ""
