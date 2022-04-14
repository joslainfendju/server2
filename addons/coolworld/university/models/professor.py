# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UniversityProfessor(models.Model):
     _name = 'university.professor'

     f_name = fields.Char('First name')
     l_name = fields.Char('Last name')
     sexe = fields.Selection([('male', 'Male'), ('female', 'Female')])
     identity_card = fields.Char('Identity Card')
     adress = fields.Text('Adress')
     birthday = fields.Date('Birthday')
     start_date = fields.Datetime('Start date')
     email = fields.Char()
     phone = fields.Char()
     
     department_id = fields.Many2one(comodel_name='university.department')
     subject_id = fields.Many2one(comodel_name='university.subject')

     classroom_ids = fields.Many2many(comodel_name='university.classroom',
                                      relation='prof_class_rel',
                                      column1='f_name',
                                      column2='name')
