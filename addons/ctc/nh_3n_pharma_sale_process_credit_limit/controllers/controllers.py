# -*- coding: utf-8 -*-
from odoo import http

# class Nh3nPharmaSaleProcessCreditLimit(http.Controller):
#     @http.route('/nh_3n_pharma_sale_process_credit_limit/nh_3n_pharma_sale_process_credit_limit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_3n_pharma_sale_process_credit_limit/nh_3n_pharma_sale_process_credit_limit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_3n_pharma_sale_process_credit_limit.listing', {
#             'root': '/nh_3n_pharma_sale_process_credit_limit/nh_3n_pharma_sale_process_credit_limit',
#             'objects': http.request.env['nh_3n_pharma_sale_process_credit_limit.nh_3n_pharma_sale_process_credit_limit'].search([]),
#         })

#     @http.route('/nh_3n_pharma_sale_process_credit_limit/nh_3n_pharma_sale_process_credit_limit/objects/<model("nh_3n_pharma_sale_process_credit_limit.nh_3n_pharma_sale_process_credit_limit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_3n_pharma_sale_process_credit_limit.object', {
#             'object': obj
#         })