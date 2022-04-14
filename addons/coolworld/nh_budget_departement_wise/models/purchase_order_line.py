# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.constrains('departement_id')
    def _check_analytic_requirement(self):
        return True
