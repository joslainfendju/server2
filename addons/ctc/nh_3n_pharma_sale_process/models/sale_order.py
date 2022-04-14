# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'draft order'),
        ('sent', 'Order Sent'),
        ('sale_head_validation', 'Validated'),
        ('sale', 'Fully Validated'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        
        #('warehouse_validation','Validated by Warehouse Manager'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    sale_head_validation_date = fields.Datetime(string='Head sale Validation Date',help="Date on which the sales order is validated by Head of Sales.", copy=False)
    is_office_sale = fields.Boolean('Is a sale fo Head Office',compute="_get_is_office_sale")

    have_branch = fields.Boolean('Have branch?',compute="_get_have_branch")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange',
                              default=lambda self: False)

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        flag = False
        if not self.user_id:
            flag = True
        super(sale_order,self).onchange_partner_id()
        """
            pour avoir l'utilisateur par defaut, nous commentons la ligne suivante
        """
        """
        if flag:
            self.write({'user_id': False})
        """

    @api.model
    def create(self, vals):

        res =super(sale_order,self).create(vals)
        """
        pour avoir l'utilisateur par defaut, nous commentons la ligne suivante
        """
        """if ('user_id' in vals and not vals['user_id']):
            res.write({'user_id':False})
        """
        return res


    def _get_is_office_sale(self):
        for rec in self:
            if rec.branch_id and rec.branch_id.is_office_branch:
                rec.is_office_sale=True
            else:
                rec.is_office_sale=False

    def _get_have_branch(self):
        for rec in self:
            if rec.branch_id:
                rec.have_branch=True
            else:
                rec.have_branch=False

    @api.multi
    def _action_sale_head_validation(self):
        self.check_availble_qty()
        self.write({
            'state': 'sale_head_validation',
            'sale_head_validation_date': fields.Datetime.now()
        })
        #return True

    @api.multi
    def action_sale_head_validation(self):
        self.check_availble_qty()
        self._action_sale_head_validation()
    @api.multi
    def action_sale_head_validation_with_confirm(self):
        self.check_availble_qty()
        self.action_sale_head_validation()
        self.action_confirm()
      

    @api.multi
    def write(self, values):
        #if 'branch_id' in values:
            #branch=self.env['res.branch'].search([('id','=',values['branch_id'])])
            #if not branch.is_office_branch:
            #    values.update({'state':'sale_head_validation','sale_head_validation_date': fields.Datetime.now()})
        return super(sale_order,self).write(values)
    @api.model
    def create(self, vals):
        res=super(sale_order,self).create(vals)
        
        #if not res.branch_id.is_office_branch:
        #    res.action_sale_head_validation()
        return res


    @api.multi
    def check_availble_qty(self):
        for line in self.order_line:
            line.check_availble_qty()



# class nh_3n_pharma_sale_process(models.Model):
#     _name = 'nh_3n_pharma_sale_process.nh_3n_pharma_sale_process'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100