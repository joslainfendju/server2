# -*- coding: utf-8 -*-
from odoo import http

# class NhQrPickerk(http.Controller):
#     @http.route('/nh_qr_picker/nh_qr_picker/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_qr_picker/nh_qr_picker/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_qr_picker.listing', {
#             'root': '/nh_qr_picker/nh_qr_picker',
#             'objects': http.request.env['nh_qr_picker.nh_qr_picker'].search([]),
#         })

#     @http.route('/nh_qr_picker/nh_qr_picker/objects/<model("nh_qr_picker.nh_qr_picker"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_qr_picker.object', {
#             'object': obj
#         })