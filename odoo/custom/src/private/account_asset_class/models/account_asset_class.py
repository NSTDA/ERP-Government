# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv import expression


class AccountAssetClass(models.Model):
    _name = "account.asset.class"
    _description = "Asset Class"
    _check_company_auto = True

    asset_ids = fields.One2many(
        comodel_name="account.asset",
        inverse_name="class_id",
        string="Assets",
        copy=False,
        check_company=True,
    )
    name = fields.Char(required=True, index=True)
    code = fields.Char(index=True)
    note = fields.Text()
    asset_profile_id = fields.Many2one(
        comodel_name="account.asset.profile",
        string="Asset Profile",
        required=True,
        index=True,
        check_company=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "name_profile_company_unique",
            "unique(name, asset_profile_id, company_id)",
            "This asset name is already used by another asset!",
        )
    ]

    def name_get(self):
        result = []
        params = self.env.context.get("params")
        list_view = params and params.get("view_type") == "list"
        short_name_len = 16
        for rec in self:
            if rec.code:
                full_name = rec.code + " " + rec.name
                short_name = rec.code
            else:
                full_name = rec.name
                if len(full_name) > short_name_len:
                    short_name = full_name[:16] + "..."
                else:
                    short_name = full_name
            if list_view:
                name = short_name
            else:
                name = full_name
            result.append((rec.id, name))
        return result

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                ("code", "=ilike", name.split(" ")[0] + "%"),
                ("name", operator, name),
            ]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ["&", "!"] + domain[1:]
        return self._search(
            expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid
        )

    def action_view_assets(self):
        self.sudo()._read(["asset_ids"])
        asset_ids = self.asset_ids
        action = self.env.ref("account_asset_management.account_asset_action")
        action_dict = action.sudo().read()[0]
        if len(asset_ids) == 1:
            res = self.env.ref(
                "account_asset_management.account_asset_view_form", False
            )
            action_dict["views"] = [(res and res.id or False, "form")]
            action_dict["res_id"] = asset_ids.id
        elif asset_ids:
            action_dict["domain"] = [("id", "in", asset_ids.ids)]
        else:
            action_dict = {"type": "ir.actions.act_window_close"}
        return action_dict
