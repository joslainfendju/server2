import datetime
from odoo import models, fields, api, exceptions, _

class WizardBudgetReport(models.TransientModel):
    _name = 'wizard.account.move'

    move_ids = fields.Many2many('stock.move', 'wizard_account_move_rel', 'move_id', 'wizard_account_move_id',
                                string='Moves', domain="[('account_move_ids', '=', False), ('product_id', '=', 195)]")

    @api.multi
    def create_move(self):
        for move in self.move_ids:
            result = move._account_entry_move()
            mv = self.env['account.move'].search([('stock_move_id', '=', move.id)])
            mv.button_cancel()
            # date = datetime.datetime.strptime(move.date,'%d/%m/%Y %H:%M:%S')
            mv.write({'date': move.date})
            mv.post()
        return result

