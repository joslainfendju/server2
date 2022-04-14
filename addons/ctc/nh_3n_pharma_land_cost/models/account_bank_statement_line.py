# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import UserError


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'
    _name = 'account.bank.statement.line'

    order_id = fields.Many2one("purchase.order", 'Purchase Order')