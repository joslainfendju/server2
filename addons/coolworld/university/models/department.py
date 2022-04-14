# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UniversityDepartment(models.Model):
     _name = 'university.department'
     
     name = fields.Char()
     code = fields.Char()

     professor_ids = fields.One2many(comodel_name='university.professor', inverse_name='department_id')
     subject_ids = fields.One2many(comodel_name='university.subject', inverse_name='department_id')