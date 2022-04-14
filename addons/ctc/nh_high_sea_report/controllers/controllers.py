# -*- coding: utf-8 -*-
from odoo import http

# class NhHighSeaReport(http.Controller):
#     @http.route('/nh_high_sea_report/nh_high_sea_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_high_sea_report/nh_high_sea_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_high_sea_report.listing', {
#             'root': '/nh_high_sea_report/nh_high_sea_report',
#             'objects': http.request.env['nh_high_sea_report.nh_high_sea_report'].search([]),
#         })

#     @http.route('/nh_high_sea_report/nh_high_sea_report/objects/<model("nh_high_sea_report.nh_high_sea_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_high_sea_report.object', {
#             'object': obj
#         })