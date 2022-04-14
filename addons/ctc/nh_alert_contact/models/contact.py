# -*- coding: utf-8 -*-

from odoo import models, fields, api

class nh_alert_contact(models.Model):
     _name = 'nh_alert_contact.contact'

     partner_id= fields.Many2one('res.partner', 'Contact')
     branch_ids = fields.Many2many('res.branch', id1='contact_id', id2='branch_id', string='Branch')
     active = fields.Boolean('Active')
     name = fields.Char(compute="_get_name", string='Email')
     email= fields.Char(compute="_get_email", string='Email')
     phone = fields.Char(compute="_get_phone",string= 'Phone Number')

     def _get_name(self):
          for rec in self:
               rec.name = rec.partner_id.name

     def _get_email(self):
          for rec in self:
               rec.email = rec.partner_id.email

     def _get_phone(self):
          for rec in self:
               rec.phone = rec.partner_id.phone
