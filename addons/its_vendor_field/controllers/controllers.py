# -*- coding: utf-8 -*-
from odoo import http

# class ItsVendorField(http.Controller):
#     @http.route('/its_vendor_field/its_vendor_field/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/its_vendor_field/its_vendor_field/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('its_vendor_field.listing', {
#             'root': '/its_vendor_field/its_vendor_field',
#             'objects': http.request.env['its_vendor_field.its_vendor_field'].search([]),
#         })

#     @http.route('/its_vendor_field/its_vendor_field/objects/<model("its_vendor_field.its_vendor_field"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('its_vendor_field.object', {
#             'object': obj
#         })