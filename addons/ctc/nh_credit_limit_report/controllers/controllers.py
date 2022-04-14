# -*- coding: utf-8 -*-
from odoo import http

# class Nh3nPharmaListOfCustomerCreditLimitReport(http.Controller):
#     @http.route('/nh_credit_limit_report/nh_credit_limit_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_credit_limit_report/nh_credit_limit_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_credit_limit_report.listing', {
#             'root': '/nh_credit_limit_report/nh_credit_limit_report',
#             'objects': http.request.env['nh_credit_limit_report.nh_credit_limit_report'].search([]),
#         })

#     @http.route('/nh_credit_limit_report/nh_credit_limit_report/objects/<model("nh_credit_limit_report.nh_credit_limit_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_credit_limit_report.object', {
#             'object': obj
#         })