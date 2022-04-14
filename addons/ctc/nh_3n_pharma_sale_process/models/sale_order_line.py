# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class saleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    stock_available_qty = fields.Float(compute='_get_all_qty_in_stock', string='Available quantity',
                                       track_visibility='onchange')
    virtual_available_qty = fields.Float(compute='_get_all_qty_in_stock', string='Forecast Quantity')
    real_available_qty = fields.Float(compute='_get_all_qty_in_stock', string='Real available quantity',
                                      track_visibility='onchange')
    reserved_qty = fields.Float(compute='_get_all_qty_in_stock', string='Reserved quantity',
                                track_visibility='onchange')

    @api.depends('product_id', 'product_uom')
    @api.one
    def _get_all_qty_in_stock(self):
        warehouse = self.order_id.warehouse_id
        product_with_context = self.product_id.with_context(
            {'location': warehouse.lot_stock_id.id, 'product_uom': self.product_uom.id})
        self.stock_available_qty = product_with_context.qty_available
        self.stock_available_qty = self.product_id.uom_id._compute_quantity(self.stock_available_qty,
                                                                          self.product_uom,
                                                                          rounding_method='HALF-UP')
        self.virtual_available_qty = product_with_context.virtual_available
        self.virtual_available_qty = self.product_id.uom_id._compute_quantity(self.virtual_available_qty,
                                                                            self.product_uom,
                                                                            rounding_method='HALF-UP')

        self.real_available_qty = self.env['stock.quant']._get_available_quantity(product_id=self.product_id,
                                                                                 location_id=warehouse.lot_stock_id,
                                                                                 lot_id=None, package_id=None,
                                                                                 owner_id=None, strict=False,
                                                                                 allow_negative=False)

        self.real_available_qty = self.product_id.uom_id._compute_quantity(self.real_available_qty,
                                                                         self.product_uom,
                                                                         rounding_method='HALF-UP')


        self.virtual_available_qty = self.product_id.uom_id._compute_quantity(self.virtual_available_qty,
                                                                          self.product_uom,
                                                                          rounding_method='HALF-UP')


        self.reserved_qty = self.stock_available_qty - self.real_available_qty

    @api.multi
    def check_availble_qty(self):
        if self.product_id.type == 'product' and self.product_uom_qty > self.real_available_qty:
            raise UserError(_("Current Stock is insuffiscient for sastify this request: Need for more " + str(
                self.product_uom_qty - self.real_available_qty) + " " + self.product_uom.name + " of " + str(
                self.product_id.product_tmpl_id.name) + "."))

    @api.onchange('product_id', 'product_uom')
    def refresh_available_qty(self):
        warehouse = self.order_id.warehouse_id
        product_with_context = self.product_id.with_context(
            {'location': warehouse.lot_stock_id.id, 'product_uom': self.product_uom.id})
        self.stock_available_qty = product_with_context.qty_available
        self.virtual_available_qty = product_with_context.virtual_available
        self.stock_available_qty = self.product_id.uom_id._compute_quantity(self.stock_available_qty,
                                                                            self.product_uom,
                                                                            rounding_method='HALF-UP')
        self.real_available_qty = self.env['stock.quant']._get_available_quantity(product_id=self.product_id,
                                                                                  location_id=warehouse.lot_stock_id,
                                                                                  lot_id=None, package_id=None,
                                                                                  owner_id=None, strict=False,
                                                                                  allow_negative=False)

        self.real_available_qty = 150


        self.virtual_available_qty = self.product_id.uom_id._compute_quantity(self.virtual_available_qty,
                                                                            self.product_uom,
                                                                            rounding_method='HALF-UP')


        self.reserved_qty = self.stock_available_qty - self.real_available_qty
