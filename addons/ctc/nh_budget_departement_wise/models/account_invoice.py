# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def invoice_line_move_line_get(self):
        res = super(AccountInvoice, self).invoice_line_move_line_get()
        for move_line_dict in res:
            move_line_dict.update({
                'departement_id': self.departement_id.id
            })

        return res
