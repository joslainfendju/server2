# -*- coding: utf-8 -*-
from odoo import api, models


class POSSession(models.Model):
    _inherit = 'pos.session'

    @api.multi
    def get_user_data_x(self):
        return self.user_id