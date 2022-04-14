# -*- coding: utf-8 -*-
from odoo import http

# class Nh3nPharmaListOfCustomerCreditLimitReport(http.Controller):
#     @http.route('/nh_credit_limit_report_ce/nh_credit_limit_report_ce/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_credit_limit_report_ce/nh_credit_limit_report_ce/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_credit_limit_report_ce.listing', {
#             'root': '/nh_credit_limit_report_ce/nh_credit_limit_report_ce',
#             'objects': http.request.env['nh_credit_limit_report_ce.nh_credit_limit_report_ce'].search([]),
#         })

#     @http.route('/nh_credit_limit_report_ce/nh_credit_limit_report_ce/objects/<model("nh_credit_limit_report_ce.nh_credit_limit_report_ce"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_credit_limit_report_ce.object', {
#             'object': obj
#         })