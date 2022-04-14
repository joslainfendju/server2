# -*- coding: utf-8 -*-
from odoo import http

# class ItsBankRegister(http.Controller):
#     @http.route('/its_bank_register/its_bank_register/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/its_bank_register/its_bank_register/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('its_bank_register.listing', {
#             'root': '/its_bank_register/its_bank_register',
#             'objects': http.request.env['its_bank_register.its_bank_register'].search([]),
#         })

#     @http.route('/its_bank_register/its_bank_register/objects/<models("its_bank_register.its_bank_register"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('its_bank_register.object', {
#             'object': obj
#         })