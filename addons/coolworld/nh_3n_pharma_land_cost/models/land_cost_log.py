# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import logging
import datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)



class LandCostLog(models.Model):
    _name = 'nh_3n_pharma_land_cost.land_cost_log'

    product_template_id = fields.Many2one("product.template", 'Product', readonly=True)
    land_cost_id = fields.Many2one("nh_3n_pharma_land_cost.land_cost", 'Landing Cost', readonly=True)
    land_cost_line_id = fields.Many2one("nh_3n_pharma_land_cost.land_cost_line", 'Landing Cost Line', readonly=True)
    old_product_qty = fields.Float('Product quantity before Cost change' , readonly=True)
    old_product_cost = fields.Float('Product Cost price before Arrival' , readonly=True)

    landed_product_qty = fields.Float('Quantity of Landed Product' , readonly=True)
    landed_product_cost = fields.Float('Cost of Landed Product' , readonly=True)

    new_product_cost = fields.Float('New Product Cost', readonly=True)
    date_log = fields.Date('Cost update on')