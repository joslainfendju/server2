from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError

from odoo import fields, models, api

class AccountAccount (models.Model):
    _inherit = 'account.account'

    @api.multi
    def write(self, vals):
        if 'reconcile' in vals:
            vals.pop('reconcile')

        return super(AccountAccount, self).write(vals)

    @api.multi
    @api.constrains('internal_type', 'reconcile')
    def _check_reconcile(self):
        return True


