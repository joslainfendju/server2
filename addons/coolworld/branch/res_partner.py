# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class res_partner(models.Model):
    _inherit = 'res.partner'

    branch_id = fields.Many2one('res.branch', 'Branch', required=True)







