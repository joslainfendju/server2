# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
# import odoo.addons.decimal_precision as dp

class Customer_supplier_modifications(models.Model):
    _inherit = 'res.partner'
    
    type_de_client = fields.Selection([('cash', 'Cash'), ('credit', 'Credit')], 'Type of customer')
    ref_supplier = fields.Char('Registration number', readonly = True)
    salesman_responsible_id = fields.Many2one('res.users', 'Salesman responsible')
    person_to_contact = fields.Char('Person to contact')
    customer_discount = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], 'Discount', store = True)
    discount = fields.Float('Discount Rate')
    #branch_id = fields.Many2one('res.branch', 'Branch')

    @api.model
    def create(self, vals):
        if vals['customer']==True:
            code = self.env['ir.sequence'].next_by_code('SC')
            code = code[2:]
            if 'branch_id' in vals:
                code_client = self.env['res.branch'].search([('id', '=', vals['branch_id'])]).code  + '-' + code
                #code_client = self.env['res.branch'].search([('id', '=', self.branch_id)]).code  + '-' + code
            else:
                code_client = "______"

            vals['ref'] = code_client

        else:
            if vals['supplier']==True:
                code = self.env['ir.sequence'].next_by_code('SN')
                code = code[2:]
                code_client = str(vals['name'])[:3]  + '-' + code
            vals['ref'] = code_client

        if vals['customer']==False and vals['supplier']==False:
            vals['ref'] = "______"

        return super(Customer_supplier_modifications, self).create(vals)

class Customer_supplier_res_users(models.Model):
    _inherit = 'res.users'

    salesman_ids = fields.One2many('res.partner', 'salesman_responsible_id')

class customer_supplier_branch(models.Model):
    _inherit = 'res.branch'

    customer_supplier_branch_ids = fields.One2many('res.partner', 'branch_id')





