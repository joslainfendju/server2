# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Company(models.Model):
    _inherit = 'res.company'

    expense_approval_route = fields.Selection(
        selection=[
            ('no', 'No'),
            ('optional', 'Optional'),
            ('required', 'Required')
        ], string="Use Expense Approval Route", default='no')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    expense_approval_route = fields.Selection(related='company_id.expense_approval_route',
                                               string="Use Expense Approval Route", readonly=False)
