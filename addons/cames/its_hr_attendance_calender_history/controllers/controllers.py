# -*- coding: utf-8 -*-
from odoo import http

# class ItsHrAttendanceCalenderHistory(http.Controller):
#     @http.route('/its_hr_attendance_calender_history/its_hr_attendance_calender_history/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/its_hr_attendance_calender_history/its_hr_attendance_calender_history/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('its_hr_attendance_calender_history.listing', {
#             'root': '/its_hr_attendance_calender_history/its_hr_attendance_calender_history',
#             'objects': http.request.env['its_hr_attendance_calender_history.its_hr_attendance_calender_history'].search([]),
#         })

#     @http.route('/its_hr_attendance_calender_history/its_hr_attendance_calender_history/objects/<model("its_hr_attendance_calender_history.its_hr_attendance_calender_history"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('its_hr_attendance_calender_history.object', {
#             'object': obj
#         })