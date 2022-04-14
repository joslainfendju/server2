# -*- coding: utf-8 -*-
from odoo import http

# class NhInvoiceQr(http.Controller):
#     @http.route('/nh_invoice__qr/nh_invoice__qr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_invoice__qr/nh_invoice__qr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_invoice__qr.listing', {
#             'root': '/nh_invoice__qr/nh_invoice__qr',
#             'objects': http.request.env['nh_invoice__qr.nh_invoice__qr'].search([]),
#         })

#     @http.route('/nh_invoice__qr/nh_invoice__qr/objects/<model("nh_invoice__qr.nh_invoice__qr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_invoice__qr.object', {
#             'object': obj
#         })