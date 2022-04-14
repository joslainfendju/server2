# -*- coding: utf-8 -*-
from odoo import http

# class NhSalePriceControl(http.Controller):
#     @http.route('/nh_sale_price_control/nh_sale_price_control/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_sale_price_control/nh_sale_price_control/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_sale_price_control.listing', {
#             'root': '/nh_sale_price_control/nh_sale_price_control',
#             'objects': http.request.env['nh_sale_price_control.nh_sale_price_control'].search([]),
#         })

#     @http.route('/nh_sale_price_control/nh_sale_price_control/objects/<model("nh_sale_price_control.nh_sale_price_control"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_sale_price_control.object', {
#             'object': obj
#         })