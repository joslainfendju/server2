# -*- coding: utf-8 -*-


from odoo import models, fields, api
#pour les logs
import logging
class Model(models.TransientModel):
    _name = 'voucher.type.fixer'
    voucher_type_id = fields.Many2one('account.voucher.type', 'Voucher type')
    code = fields.Char('code')

    def start(self):
        for aml in self.env['account.move.line'].search([('voucher_type', '=', self.code)]):
            aml.write({'voucher_type_id': self.voucher_type_id .id})
        return True

    


