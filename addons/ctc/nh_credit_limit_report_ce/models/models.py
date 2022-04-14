# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class ResPartner(models.Model):
    _inherit = 'res.partner'

    #branch_id=fields.Many2one('res.branch','Branch')

    

    remaining_credit=fields.Float(compute='_get_remaining_credit',string='Remaining Credit')

    
    def _get_remaining_credit(self):
    	for rec in self:
        	rec.remaining_credit=max(rec.credit_limit-rec.credit,0)


