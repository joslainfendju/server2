# -*- coding: utf-8 -*-
from odoo import http

# class NhScmStockTransitReport(http.Controller):
#     @http.route('/nh_scm_stock_transit_report/nh_scm_stock_transit_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_scm_stock_transit_report/nh_scm_stock_transit_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_scm_stock_transit_report.listing', {
#             'root': '/nh_scm_stock_transit_report/nh_scm_stock_transit_report',
#             'objects': http.request.env['nh_scm_stock_transit_report.nh_scm_stock_transit_report'].search([]),
#         })

#     @http.route('/nh_scm_stock_transit_report/nh_scm_stock_transit_report/objects/<model("nh_scm_stock_transit_report.nh_scm_stock_transit_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_scm_stock_transit_report.object', {
#             'object': obj
#         })