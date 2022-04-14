# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    need_price_validation = fields.Boolean(string='Need price validation', default=False, store=True, compute='_get_need_price_validation',track_visibility='onchange')

   
    """
    @api.multi
    def write(self, vals):
        
        if 'price_unit' in vals:
            if self.order_id.pricelist_id and self.order_id.partner_id:
                real_price = self.order_id.pricelist_id.get_product_price(self.product_id,
                                                                                    self.product_uom_qty,
                                                                                    self.order_id.partner_id)
                #raise UserError(_("real price is "+str(real_price)))
                if(vals['price_unit']<real_price):
                     raise UserError(_("You can only increase the sale price"))
       
        return super(SaleOrderLine, self).write(vals)
    """

    @api.one
    def _check_sale_price_list(self):
        real_price = self.order_id.pricelist_id.get_product_price(self.product_id,self.product_uom_qty,
                                                                                             self.order_id.partner_id)
        #raise UserError(_("real price is "+str(real_price)))
        if self.order_id.pricelist_id and self.order_id.partner_id:
            #real_price = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(self.product_id), self.product_id.taxes_id, self.tax_id, self.company_id)
            #raise UserError(_("real price is "+str(real_price)))
            if(not self.is_promotion_line and self.price_unit<real_price):
                     raise UserError(_("You can only increase the sale price"))

    @api.one
    @api.depends('price_unit','order_id.pricelist_id')
    def _get_need_price_validation(self):
        need_price_validation = False
        if self.order_id.pricelist_id and self.order_id.pricelist_id.need_price_validation:
            need_price_validation = True
        elif self.order_id.pricelist_id and self.order_id.partner_id:
            real_price = real_price = self.order_id.pricelist_id.get_product_price(self.product_id,
                                                                                             self.product_uom_qty,
                                                                                             self.order_id.partner_id)
            # raise UserError(_("real price is "+str(real_price)))

            if self.order_id.pricelist_id and self.price_unit > real_price:
                need_price_validation = True

        #rec.write({'need_price_validation' : need_price_validation})
        self.need_price_validation = need_price_validation
        if need_price_validation:
            self.order_id.write({'price_validated': False})




        


