
from odoo import fields, models, api


class ProductUoM(models.Model):
    _inherit = 'product.uom'

    factor = fields.Float(digits=(42, 15))
