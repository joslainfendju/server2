# -*- coding: utf-8 -*-
from odoo import http

# class Nh3nPharmaSaleProcess(http.Controller):
#     @http.route('/nh_3n_pharma_sale_process/nh_3n_pharma_sale_process/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_3n_pharma_sale_process/nh_3n_pharma_sale_process/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_3n_pharma_sale_process.listing', {
#             'root': '/nh_3n_pharma_sale_process/nh_3n_pharma_sale_process',
#             'objects': http.request.env['nh_3n_pharma_sale_process.nh_3n_pharma_sale_process'].search([]),
#         })

#     @http.route('/nh_3n_pharma_sale_process/nh_3n_pharma_sale_process/objects/<model("nh_3n_pharma_sale_process.nh_3n_pharma_sale_process"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_3n_pharma_sale_process.object', {
#             'object': obj
#         })