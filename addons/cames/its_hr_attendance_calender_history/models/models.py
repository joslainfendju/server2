# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployeeCalendarLog(models.Model):
    _name = 'hr.employee.calendar.log'
    calendar_id = fields.Many2one('resource.calendar')
    employee_ids = fields.One2many('hr.employee')
    calendar_used_date = fields.Datetime()


