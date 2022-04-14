# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

# class nh_available_qty_on_stock_picking(models.Model):
#     _name = 'nh_available_qty_on_stock_picking.nh_available_qty_on_stock_picking'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class MouvementStock(models.Model):
    _inherit='stock.move'

    quantiteEnStock=fields.Integer(string="quantity available",compute="_quantite_en_stock", store=False)

    @api.depends('product_id','location_id')
    def _quantite_en_stock(self):
        for rec in self:
            rec.quantiteEnStock=rec.product_id.with_context({'location':rec.location_id.id}).qty_available

class OperationDeStock(models.Model):
    _inherit='stock.picking'

    @api.multi
    def do_new_transfer(self):
       
        for pick in self:

            for operation in pick.pack_operation_ids:
                location=operation.picking_source_location_id
                if(location and location.usage!='supplier'and location.usage!='customer'):
                    if(operation.pack_lot_ids):
                        for lot in operation.pack_lot_ids:
                            available_qty=operation.product_id.with_context({'location':location.id,'lot_id':lot.id}).qty_available
                            if operation.product_qty < available_qty:
                                raise UserError(_('The available qty in stock is '+str(available_qty)+' for the Serial/Lot '+lot.name+' of '+operation.product_id.product_tmpl_id.name+' and is less than '+str(operation.product_qty)))
                    else:
                        available_qty=operation.product_id.with_context({'location':location.id}).qty_available
                        if operation.product_qty < available_qty:
                            raise UserError(_('The available qty in stock is '+str(available_qty)+' for '+operation.product_id.product_tmpl_id.name+' and is less than '+str(operation.product_qty)))
        res=super(OperationDeStock,self).do_new_transfer()
        return res
