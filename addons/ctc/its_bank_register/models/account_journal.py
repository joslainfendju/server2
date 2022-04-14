# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    """
       ajout du type de journal registre pour permettre de sélectionner le compte de la banque ou de la caisse
       sur la ligne du rélévé bancaire ou sur la ligne de caisse
    """
    type = fields.Selection([
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('general', 'Miscellaneous'),
        ("sale_refund", "Customer refund"),
        ("purchase_refund", "Supplier refund"),
        ('register', 'Transaction Register'),
    ], required=True,
        help="Select 'Sale' for customer invoices journals.\n" \
             "Select 'Purchase' for vendor bills journals.\n" \
             "Select 'Cash' or 'Bank' for journals that are used in customer or vendor payments.\n" \
             "Select 'register' for pass transaction for various bank on cash account in the same journal.\n" \
             "Select 'General' for miscellaneous operations journals.")

    branch_id = fields.Many2one('res.branch', 'Branch')
    voucher_type_ids = fields.Many2many('account.voucher.type', id1='voucher_type_id', id2='journal_id', string="available voucher types")
    countepart_account_ids = fields.Many2many('account.account', id1='coutepart_id', id2='journal_id', string="Countepart account")


    def _graph_title_and_key(self):
        """
        neccessaire pour l'affichage d'un registre dans le tableau de bord
        :return: 
        """
        if self.type == 'register':
            return ['', _('Register: Balance')]
        return super(AccountJournal, self)._graph_title_and_key()

    @api.multi
    def open_action(self):
        """return action based on type for related journals"""
        if self.type == 'register':
            action_name = 'action_bank_statement_tree'

            ctx = self._context.copy()
            ctx.pop('group_by', None)
            ctx.update({
                'journal_type': self.type,
                'default_journal_id': self.id,
                'default_type': 'register',
                'type': 'register'
            })

            [action] = self.env.ref('account.%s' % action_name).read()
            if not self.env.context.get('use_domain'):
                ctx['search_default_journal_id'] = self.id
            action['context'] = ctx
            action['domain'] = self._context.get('use_domain', [])

            return action

        else:
            return  super(AccountJournal, self).open_action()