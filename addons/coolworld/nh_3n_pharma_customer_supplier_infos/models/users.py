# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
# import odoo.addons.decimal_precision as dp

class Users(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):


        user = super(Users, self).create(vals)
        user.partner_id.write({
                                'customer' : False,
                                'supplier' : False,
                                'branch_id' : user.branch_id.id
                                })
        return  user

