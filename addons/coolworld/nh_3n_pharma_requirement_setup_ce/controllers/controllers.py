# -*- coding: utf-8 -*-
from odoo import http

# class Nh3nPharmaRequirementSetup(http.Controller):
#     @http.route('/nh_3n_pharma_requirement_setup/nh_3n_pharma_requirement_setup/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_3n_pharma_requirement_setup/nh_3n_pharma_requirement_setup/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_3n_pharma_requirement_setup.listing', {
#             'root': '/nh_3n_pharma_requirement_setup/nh_3n_pharma_requirement_setup',
#             'objects': http.request.env['nh_3n_pharma_requirement_setup.nh_3n_pharma_requirement_setup'].search([]),
#         })

#     @http.route('/nh_3n_pharma_requirement_setup/nh_3n_pharma_requirement_setup/objects/<model("nh_3n_pharma_requirement_setup.nh_3n_pharma_requirement_setup"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_3n_pharma_requirement_setup.object', {
#             'object': obj
#         })