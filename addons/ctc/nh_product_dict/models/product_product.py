# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class ProductProduct(models.Model):
    _inherit = 'product.product'

    volume = fields.Float('Volume', help="The volume in m3.", digits=(32, 10))
    weight = fields.Float('Weight', help="The weight of the contents in Kg, not including any packaging, etc.",
                          digits=(32, 10))
