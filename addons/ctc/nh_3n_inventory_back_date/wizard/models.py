# -*- coding: utf-8 -*-


from odoo import models, fields, api,_
from openerp.exceptions import ValidationError

import csv


class Model(models.TransientModel):
    _name = 'inventory.date.correct'

    #branch_id = fields.Many2one('res.branch', 'Branch')
    code = fields.Char('Line-code')
    date = fields.Datetime('correct date')
    inventory_id = fields.Many2one('stock.inventory', 'Inventaire')
    branch_date_correct = fields.Boolean('Branch-date-correct',default=False,help="If check branch and date will be correcte,\nthe new date will be the provided"
                                                                          "Else only the inventory will be correct to new date")



    def start(self):

        if self.branch_date_correct:
            for acm in self.env['account.move'].search([('journal_id.code','=','STJ')]):
                for aml in acm.line_ids:
                    if self.code in aml.name and 'INV:' in aml.name:
                        #aml.write({'branch_id':self.branch_id.id})
                        aml.write({'date': self.date})
                       # acm.write({'branch_id':self.branch_id.id })
                        acm.write({'date': self.date})

        return True

    def update_inventory(self):
            for inv in self.env['stock.inventory'].search([('id','=',self.inventory_id.id)]):
                for invl in inv.line_ids:
                    invl.write({'date': self.date})
                inv.write({'date': self.date})
                related_moves=self.env['stock.move'].search([('inventory_id','=',inv.id)])
                for mv in related_moves:
                    mv.write({'date': self.date})
                    mv.write({'date_expected': self.date})
                    for mvl in mv.move_line_ids:
                        mvl.write({'date': self.date})


            return True












