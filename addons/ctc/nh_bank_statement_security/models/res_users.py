# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    journal_ids = fields.Many2many('account.journal', 'journal_id', string='Branch')

    @api.multi
    def write(self, values):
        if 'journal_id' in values or 'journal_ids' in values:
            self.env['ir.model.access'].call_cache_clearing_methods()
            self.env['ir.rule'].clear_caches()
            self.has_group.clear_cache(self)
        user = super(ResUsers, self).write(values)
        return user
