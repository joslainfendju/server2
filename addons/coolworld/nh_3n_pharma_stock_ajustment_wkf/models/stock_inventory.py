# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_utils


class Inventory(models.Model):
    _inherit = "stock.inventory"


    state = fields.Selection(string='Status', selection=[
        ('draft', 'Draft'),
        ('cancel', 'Cancelled'),
        ('confirm', 'In Progress'),
        ('first_level_validation', 'Validation MD'),
        ('second_level_validation', 'Validation GM'),
        ('done', 'Validated')],
                             copy=False, index=True, readonly=True,
                             default='draft')

    date_first_level_validation = fields.Date('MD validation date')
    date_second_level_validation = fields.Date('GM validation date')


    @api.multi
    def button_first_level_validation(self):
        self.write({
            'state': 'first_level_validation',
            'date_first_level_validation': fields.Datetime.now()
        })

    @api.multi
    def button_second_level_validation(self):
        self.write({
            'state': 'second_level_validation',
            'date_second_level_validation': fields.Datetime.now()
        })
        return self.action_done()