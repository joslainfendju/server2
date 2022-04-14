# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re
from odoo.exceptions import UserError
# import odoo.addons.decimal_precision as dp

class Partner(models.Model):
    _inherit = 'res.partner'


    tax_payer_number = fields.Char(string='Tax Payer Number', help="Tax Identification Number."
                                                      "Fill it if the company is subjected to taxes. "
                                                      "Used by the some of the legal statements.")
    registration_number = fields.Char(string='Registration Number')
    customer_type = fields.Selection([('cash', 'Cash'), ('credit', 'Credit')], 'Type of customer')
    user_id = fields.Many2one('res.users', string='Salesman responsible',
                              help='The internal user that is in charge of communicating with this contact if any.')
    branch_id = fields.Many2one('res.branch', 'Branch', required=False)




    @api.model
    def create(self, vals):


        if vals['customer'] == True:
            code = self.env['ir.sequence'].next_by_code('SC')
            code_client = code
            if 'branch_id' in vals:
                branch = self.env['res.branch'].search([('id', '=', vals['branch_id'])])
                if branch :
                    code_client = branch.code + '-' +  code[2:]

            vals['ref'] = code_client

        elif vals['supplier'] == True:
                code = self.env['ir.sequence'].next_by_code('SS')
                code = code[2:]
                code_four = str(vals['name'])[:3]
                vals['ref'] = code_four + '-' + code
        else:
            code = self.env['ir.sequence'].next_by_code('OP')
            vals['ref'] = code[2:]

        return super(Partner, self).create(vals)


    @api.constrains('name')
    def check_name(self):
        #if not bool(re.match('^[a-zA-Zéèp ]+$', self.name)):
        #     raise UserError(_("Invalid Character in customer name"))
        return True

