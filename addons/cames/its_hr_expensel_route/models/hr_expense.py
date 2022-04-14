# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Expense(models.Model):
    _inherit = "hr.expense"

    @api.onchange('product_id')
    def get_domain_uom(self):
        if not self.product_id:
            uoms = self.env['product.uom'].search([('id', '>', 0)])
            domain = {'product_uom_id': [('id', '>', 0)]}
            result = {'domain': domain, 'value': {'product_uom_id': uoms[0]}}

            return result

        select_product = self.product_id
        uoms = self.env['product.uom'].search([('category_id', '=', select_product.uom_id.category_id.id)])

        domain = {'product_uom_id': [('category_id', '=', select_product.uom_id.category_id.id)]}
        result = {'domain': domain, 'value': {'product_uom_id': uoms[0]}}

        return result
