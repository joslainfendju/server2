# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

   

    @api.multi
    def write(self, vals):
        
        if 'price_unit' in vals:
            if self.order_id.pricelist_id and self.order_id.partner_id:
                real_price = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(self.product_id), self.product_id.taxes_id, self.tax_id, self.company_id)
                #raise UserError(_("real price is "+str(real_price)))
                if(vals['price_unit']<real_price):
                     raise UserError(_("You can only increase the sale price"))
       
        return super(SaleOrderLine,self).write(vals)


    @api.constrains('price_unit')
    def _sale_price_list(self):
      
        real_price = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(self.product_id), self.product_id.taxes_id, self.tax_id, self.company_id)
        #raise UserError(_("real price is "+str(real_price)))

        if self.order_id.pricelist_id and self.order_id.partner_id:
            #real_price = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(self.product_id), self.product_id.taxes_id, self.tax_id, self.company_id)
            #raise UserError(_("real price is "+str(real_price)))
            if(self.price_unit<real_price):
                     raise UserError(_("You can only increase the sale price"))
        


