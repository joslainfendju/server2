# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    """
       le type de la transaction
    """
    voucher_type = fields.Char('Voucher type value')
    voucher_type_id = fields.Many2one('account.voucher.type', 'Voucher type')
    voucher_type_ids = fields.Many2many(compute='_get_voucher_type_ids')

    @api.one
    @api.depends('create_date', 'journal_id', 'move_id.journal_id')
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



    def create(self, vals):
        """
        Mise à jour du type de transaction en fonction de celle spécifiée sur le paiement ou sur la ligne de caisse
        :param vals:
        :return:
        """
        if 'statement_line_id' in vals:
            statement_line = self.env['account.bank.statement.line'].browse([vals['statement_line_id']])[0]
            if statement_line and statement_line.voucher_type_id:
                vals.update({'voucher_type': statement_line.voucher_type,
                             'voucher_type_id': statement_line.voucher_type_id.id })
        elif 'payment_id' in vals:
            payment = self.env['account.payment'].browse([vals['payment_id']])[0]
            if payment and payment.voucher_type_id:
                vals.update({'voucher_type': payment.voucher_type, 'voucher_type_id': payment.voucher_type_id.id})
        return super(AccountMoveLine, self).create(vals)
