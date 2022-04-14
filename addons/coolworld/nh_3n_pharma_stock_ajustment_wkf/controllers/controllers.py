# -*- coding: utf-8 -*-
from odoo import http

# class Nh3nPharmaStockAjustmentWkf(http.Controller):
#     @http.route('/nh_3n_pharma_stock_ajustment_wkf/nh_3n_pharma_stock_ajustment_wkf/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_3n_pharma_stock_ajustment_wkf/nh_3n_pharma_stock_ajustment_wkf/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_3n_pharma_stock_ajustment_wkf.listing', {
#             'root': '/nh_3n_pharma_stock_ajustment_wkf/nh_3n_pharma_stock_ajustment_wkf',
#             'objects': http.request.env['nh_3n_pharma_stock_ajustment_wkf.nh_3n_pharma_stock_ajustment_wkf'].search([]),
#         })

#     @http.route('/nh_3n_pharma_stock_ajustment_wkf/nh_3n_pharma_stock_ajustment_wkf/objects/<model("nh_3n_pharma_stock_ajustment_wkf.nh_3n_pharma_stock_ajustment_wkf"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_3n_pharma_stock_ajustment_wkf.object', {
#             'object': obj
#         })