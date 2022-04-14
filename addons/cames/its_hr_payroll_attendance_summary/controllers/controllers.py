# -*- coding: utf-8 -*-
from odoo import http

# class ItsHrPayrollAttendanceSummary(http.Controller):
#     @http.route('/its_hr_payroll_attendance_summary/its_hr_payroll_attendance_summary/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/its_hr_payroll_attendance_summary/its_hr_payroll_attendance_summary/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('its_hr_payroll_attendance_summary.listing', {
#             'root': '/its_hr_payroll_attendance_summary/its_hr_payroll_attendance_summary',
#             'objects': http.request.env['its_hr_payroll_attendance_summary.its_hr_payroll_attendance_summary'].search([]),
#         })

#     @http.route('/its_hr_payroll_attendance_summary/its_hr_payroll_attendance_summary/objects/<model("its_hr_payroll_attendance_summary.its_hr_payroll_attendance_summary"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('its_hr_payroll_attendance_summary.object', {
#             'object': obj
#         })