# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_invoice_policy = fields.Selection([
            ('order', 'Invoice what is ordered'),
            ('delivery', 'Invoice what is delivered')
            ], 'Invoicing Policy',
            default='delivery',
            default_model='product.template')