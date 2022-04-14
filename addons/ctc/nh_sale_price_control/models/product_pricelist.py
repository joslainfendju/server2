# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class ProductPricelist(models.Model):
    _name = 'product.pricelist'
    _inherit = 'product.pricelist'

    need_price_validation = fields.Boolean(string='Need validation', default=False)
