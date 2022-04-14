# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def _check_department_msg(self):
        for line in self.line_ids:
            line._check_department_msg()

        return True
