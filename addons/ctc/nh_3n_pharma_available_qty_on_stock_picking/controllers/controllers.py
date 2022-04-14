# -*- coding: utf-8 -*-
from odoo import http

# class NhAvailableQtyOnStockPicking(http.Controller):
#     @http.route('/nh_available_qty_on_stock_picking/nh_available_qty_on_stock_picking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_available_qty_on_stock_picking/nh_available_qty_on_stock_picking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_available_qty_on_stock_picking.listing', {
#             'root': '/nh_available_qty_on_stock_picking/nh_available_qty_on_stock_picking',
#             'objects': http.request.env['nh_available_qty_on_stock_picking.nh_available_qty_on_stock_picking'].search([]),
#         })

#     @http.route('/nh_available_qty_on_stock_picking/nh_available_qty_on_stock_picking/objects/<model("nh_available_qty_on_stock_picking.nh_available_qty_on_stock_picking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_available_qty_on_stock_picking.object', {
#             'object': obj
#         })