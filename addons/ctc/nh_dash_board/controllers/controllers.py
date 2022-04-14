# -*- coding: utf-8 -*-
from odoo import http

# class NhDashBoard(http.Controller):
#     @http.route('/nh_dash_board/nh_dash_board/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_dash_board/nh_dash_board/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_dash_board.listing', {
#             'root': '/nh_dash_board/nh_dash_board',
#             'objects': http.request.env['nh_dash_board.nh_dash_board'].search([]),
#         })

#     @http.route('/nh_dash_board/nh_dash_board/objects/<model("nh_dash_board.nh_dash_board"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_dash_board.object', {
#             'object': obj
#         })