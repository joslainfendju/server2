# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountPayment(models.Model):
    _inherit = 'account.payment'


    operation_account_id = fields.Many2one('account.account', string='Operation Counterpart Account',
                                           help="This  ,account will be use during reconciliation for journal "
                                                "of the type register")

    journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True,
                                 domain=[('type', 'in', ('bank', 'cash', 'register'))])

    voucher_type = fields.Char('Voucher type value')
    voucher_type_id = fields.Many2one('account.voucher.type', 'Voucher type')
    voucher_type_ids = fields.Many2many(compute='_get_voucher_type_ids')

    @api.one
    @api.depends('create_date', 'journal_id')
    def _get_voucher_type_ids(self):

        journal = self.journal_id
        if not journal:
            journal = self.move_id.journal_id
        list = [x.id for x in journal.voucher_type_ids]
        self.voucher_type_ids = [(6, 0, list)]

    @api.onchange('voucher_type_id')
    def on_voucher_type_id_change(self):
        if self.voucher_type_id:
            result = {'value': {'voucher_type': self.voucher_type_id.code}}
            return result



    def _get_liquidity_move_line_vals(self, amount):
        res = super(AccountPayment, self)._get_liquidity_move_line_vals(amount)
        if 'account_id' in res and self.journal_id.type in ['register',]:
           res.update({'account_id': self.operation_account_id.id})
        return res



