# -*- coding: utf-8 -*-


from odoo import models, fields, api
#pour les logs
import logging





class Model(models.TransientModel):
    _name = 'inventory.correct'



    branch_id = fields.Many2one('res.branch', 'Branch')
    code = fields.Char('Line-code')

    def start(self):

        for acm in self.env['account.move'].search([('branch_id','=',False),('journal_id.code','=','STJ')]):
            for aml in acm.line_ids:
                if self.code in aml.name and 'INV:' in aml.name:
                    aml.write({'branch_id':self.branch_id.id})
                    acm.write({'branch_id': self.branch_id.id})



        return True

    


