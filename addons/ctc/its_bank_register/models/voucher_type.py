# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VoucherType(models.Model):
    _name = 'account.voucher.type'

    code = fields.Char(string="Code",  help="This is the short  name of the voucher type")
    name = fields.Char(string="Transaction type",  help="This is the visible name of the voucher type")

