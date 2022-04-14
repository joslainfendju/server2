# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountBankStatement(models.Model):
    _name = 'account.bank.statement'
    _inherit = ['account.bank.statement', 'mail.thread',
                'mail.activity.mixin', 'portal.mixin']

    state = fields.Selection(
        [('open', 'New'),
         ('confirm', 'Validated')],
        string='Status',
        required=True,
        readonly=True,
        copy=False,
        default='open',
        track_visibility='onchange')
