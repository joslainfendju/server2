# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    departement_id = fields.Many2one('hr.department', 'Department')
    account_analytic_id = fields.Many2one('account.analytic.account', 'Analytic_account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')

    def _prepare_reconciliation_move_line(self, move, amount):
        """ Mis à jour des paramètres analytiques sur les écritures analytiques à génerer.

            :param recordset move: the account.move to link the move line
            :param float amount: the amount of transaction that wasn't already reconciled
        """
        res = super(AccountBankStatementLine, self)._prepare_reconciliation_move_line(move, amount)
        res.update({
            'analytic_account_id': self.account_analytic_id.id,
            'departement_id': self.departement_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)]
        })

        return res
