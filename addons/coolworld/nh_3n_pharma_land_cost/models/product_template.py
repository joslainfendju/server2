# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import logging
import datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)



class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    land_cost_log_ids = fields.One2many('nh_3n_pharma_land_cost.land_cost_log', 'product_template_id', 'Cost Price History')
    control_expense = fields.Boolean('Control expenses')


