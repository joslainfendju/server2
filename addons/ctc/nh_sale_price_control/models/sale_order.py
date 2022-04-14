# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    need_price_validation = fields.Boolean(string='Need price validation', default=False, compute='_get_need_price_validation',track_visibility='onchange')

    price_validated = fields.Boolean(string='Price Validated')
    price_validation_date = fields.Datetime(string='Price Validation Date')

    @api.one
    @api.depends('pricelist_id', 'order_line')
    def _get_need_price_validation(self):
        for line in self.order_line:
            if line.need_price_validation:
                self.need_price_validation = True
                #rec.write({'need_price_validation' : True})
                break

    @api.multi
    def _action_confirm(self):
        if self.need_price_validation and not self.price_validated:
            raise UserError(_("Price validation is required for this sale"))
        else :
            super(SaleOrder, self)._action_confirm()

    @api.multi
    def action_price_validation(self):
        self.write({
            'price_validated': True,
            'price_validation_date': fields.Datetime.now()
        })

    @api.multi
    def _action_sale_head_validation(self):
        if self.need_price_validation and not self.price_validated:
            raise UserError(_("Price validation is required for this sale"))
        else :
            super(SaleOrder, self)._action_sale_head_validation()

    @api.one
    @api.constrains('pricelist_id', 'order_line')
    def _check_sale_price_list(self):
        for line in self.order_line:
            line._check_sale_price_list()

