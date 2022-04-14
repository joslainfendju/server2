# -*- coding: utf-8 -*-
from odoo import http

# class Nh3nPharmaLandCost(http.Controller):
#     @http.route('/nh_3n_pharma_land_cost/nh_3n_pharma_land_cost/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_3n_pharma_land_cost/nh_3n_pharma_land_cost/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_3n_pharma_land_cost.listing', {
#             'root': '/nh_3n_pharma_land_cost/nh_3n_pharma_land_cost',
#             'objects': http.request.env['nh_3n_pharma_land_cost.nh_3n_pharma_land_cost'].search([]),
#         })

#     @http.route('/nh_3n_pharma_land_cost/nh_3n_pharma_land_cost/objects/<model("nh_3n_pharma_land_cost.nh_3n_pharma_land_cost"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_3n_pharma_land_cost.object', {
#             'object': obj
#         })