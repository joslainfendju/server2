# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


def get_ancestors_names(item):
    name = item.name
    parent = item.parent_id
    while parent:
        name = parent.name + ' / ' + name
        parent = parent.parent_id
    return name


class ProductTemplate(models.Model):
    _name = 'product.family'

    name = fields.Char('Name', index=True)
    display_name = fields.Char('Display Name', compute='_compute_display_name')
    parent_id = fields.Many2one('product.family', string='Parent Family')

    @api.multi
    def _compute_display_name(self):
        for item in self:
            item.display_name = get_ancestors_names(item)