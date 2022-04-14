from odoo import fields, models, api,_
from odoo.exceptions import UserError, ValidationError

class AccountGroup(models.Model):
    _inherit ="account.group"

    @api.multi
    def search_real_parent(self):
        group = False
        if self.code_prefix:
            n = len(self.code_prefix)
            i = 1
            while i < n and not group:
                code_prefix = self.code_prefix[:-i]
                group = self.search([('code_prefix', '=', code_prefix)])
                i += 1
        return group


class AccountAccount(models.Model):
    _inherit = "account.account"



    @api.multi
    def search_group(self):
        n = len(self.code)
        i = 1
        group = False
        while i < n and not group:
            code_prefix = self.code[:-i]
            group = self.env['account.group'].search([('code_prefix', '=', code_prefix)])
            i += 1
        return group