# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    """
       le type de la transaction
    """
    voucher_type = fields.Char('Voucher type value')
    voucher_type_id = fields.Many2one('account.voucher.type', 'Transaction type')

    operation_account_id = fields.Many2one('account.account', string='Operation Counterpart Account',
                                 help="This  ,account will be use during reconciliation for journal "
                                      "of the type register")
    journal_type = fields.Char(compute="_get_journal_type")
    voucher_type_ids = fields.Many2many(compute='_get_voucher_type_ids')
    countepart_account_ids = fields.Many2many(compute='_get_countepart_account_ids')

    @api.onchange('voucher_type_id')
    def on_voucher_type_id_change(self):
        if self.voucher_type_id:
            result = {'value': {'voucher_type': self.voucher_type_id.code}}
            return result

    @api.one
    @api.depends('create_date', 'statement_id.journal_id')
    def _get_voucher_type_ids(self):

        journal = self.statement_id.journal_id
        list = [x.id for x in journal.voucher_type_ids]
        self.voucher_type_ids = [(6, 0, list)]

    @api.one
    @api.depends('create_date', 'statement_id.journal_id')
    def _get_countepart_account_ids(self):

        journal = self.statement_id.journal_id
        list = [x.id for x in journal.countepart_account_ids]
        self.countepart_account_ids = [(6, 0, list)]

    @api.one
    def _get_journal_type(self):
        self.journal_type = self.journal_id and self.journal_id.type or self.statement_id.journal_id.type

    def process_reconciliation(self, counterpart_aml_dicts=None, payment_aml_rec=None, new_aml_dicts=None):
        """
        ici, il est question pour nous de retrouver les paiements créés après la réconciliation et de mettre à jour
        leur type de transaction en fonction de celui de la pièce comptable
        :param counterpart_aml_dicts:
        :param payment_aml_rec:
        :param new_aml_dicts:
        :return:
        """
        account_moves = super(AccountBankStatementLine, self).process_reconciliation(counterpart_aml_dicts,
                                                                           payment_aml_rec, new_aml_dicts)
        move_lines = self.env['account.move.line'].search([('move_id','in',[move.id for move in account_moves ])])
        for line in move_lines:
            line.payment_id.write({'voucher_type': line.voucher_type,
                                   'voucher_type_id': line.voucher_type_id.id})

    def _prepare_reconciliation_move_line(self, move, amount):
        """ Pour choisir le compte sur la ligne de caisse lorsqu'il s'agit d'un journal de type registre.

            :param recordset move: the account.move to link the move line
            :param float amount: the amount of transaction that wasn't already reconciled
        """
        res = super(AccountBankStatementLine, self)._prepare_reconciliation_move_line(move,amount)

        if 'account_id' in res and self.journal_id and self.journal_id.type in ['register',]:
            if not self.operation_account_id:
                raise UserError(_('Couterpart account have not been chosen for the statement line.'))
            res.update({'account_id': self.operation_account_id.id})

        return res
