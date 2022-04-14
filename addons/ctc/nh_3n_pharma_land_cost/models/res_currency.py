# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import math
import re
import time

from odoo import api, fields, models, tools, _


class Currency(models.Model):
    _inherit = "res.currency"

    rate = fields.Float(compute='_compute_current_rate', string='Current Rate', digits=(12, 32),
                        help='The rate of the currency to the currency of rate 1.')


class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    rate = fields.Float(digits=(12, 32), help='The rate of the currency to the currency of rate 1')
