# -*- coding: utf-8 -*-
from odoo import http

# class NhAccountChartImport(http.Controller):
#     @http.route('/nh_account_chart_import/nh_account_chart_import/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_account_chart_import/nh_account_chart_import/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_account_chart_import.listing', {
#             'root': '/nh_account_chart_import/nh_account_chart_import',
#             'objects': http.request.env['nh_account_chart_import.nh_account_chart_import'].search([]),
#         })

#     @http.route('/nh_account_chart_import/nh_account_chart_import/objects/<model("nh_account_chart_import.nh_account_chart_import"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_account_chart_import.object', {
#             'object': obj
#         })