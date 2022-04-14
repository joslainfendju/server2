# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    ref = fields.Char(string='Reference', required=True)

    @api.constrains('ref', 'statement_id')
    def _check_default_code(self):
        ref = self.search([('ref', '=ilike', self.ref)])
        if len(ref) > 1:
            raise ValidationError(_("Reference must be unique per statement!"))
