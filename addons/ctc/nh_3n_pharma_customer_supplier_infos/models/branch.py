# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
# import odoo.addons.decimal_precision as dp


class Branch(models.Model):

    _inherit = 'res.branch'
    partner_ids = fields.One2many('res.partner', 'branch_id')

