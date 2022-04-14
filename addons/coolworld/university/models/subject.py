# -*- coding: utf-8 -*-

from odoo import models, fields, api


class UniversitySubject(models.Model):
    _name = 'university.subject'

    name = fields.Char()
    code = fields.Char()

    department_id = fields.Many2one(comodel_name='university.department')
    
    