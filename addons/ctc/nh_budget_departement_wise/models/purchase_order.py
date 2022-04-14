# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.constrains('departement_id')
    def _check_analytic_requirement(self):
        return True
