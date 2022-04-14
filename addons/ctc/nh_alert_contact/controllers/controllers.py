# -*- coding: utf-8 -*-
from odoo import http

# class NhAlertContact(http.Controller):
#     @http.route('/nh_alert_contact/nh_alert_contact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nh_alert_contact/nh_alert_contact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nh_alert_contact.listing', {
#             'root': '/nh_alert_contact/nh_alert_contact',
#             'objects': http.request.env['nh_alert_contact.nh_alert_contact'].search([]),
#         })

#     @http.route('/nh_alert_contact/nh_alert_contact/objects/<model("nh_alert_contact.nh_alert_contact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nh_alert_contact.object', {
#             'object': obj
#         })