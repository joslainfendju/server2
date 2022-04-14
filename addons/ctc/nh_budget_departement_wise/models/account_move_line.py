# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    departement_id = fields.Many2one('hr.department', 'Department')

    @api.one
    def _prepare_analytic_line(self):
        """ Prepare the values used to create() an account.analytic.line upon validation of an account.move.line having
            an analytic account. This method is intended to be extended in other modules.
        """
        res = super(AccountMoveLine, self)._prepare_analytic_line()
        import logging
        logging.info("res is %s" % (res))
        if res and len(res) == 1:
            res[0].update({
                'departement_id': self.departement_id.id,

            })
        return res[0]

    @api.multi
    @api.constrains('departement_id')
    def _check_department_msg(self):
        """
        This function purpose is to require department when analytic policy is always
        :return:
        """
        for move_line in self:
            analytic_policy = move_line.account_id.analytic_policy
            if analytic_policy == 'always':
                if not move_line.departement_id:
                    raise UserError(
                        _("Department is required for this operation using account '%s - %s with description as %s'.")
                        % (move_line.account_id.code,
                           move_line.account_id.name,
                           move_line.name))
        return True

    @api.model
    def create(self, vals):
        statement_line = False
        invoice = False
        if 'statement_line_id' in vals and vals['statement_line_id']:
            statement_line = self.env['account.bank.statement.line'].search([('id', '=', vals['statement_line_id'])])
        if 'invoice_id' in vals and vals['invoice_id']:
            invoice = self.env['account.invoice'].search([('id', '=', vals['invoice_id'])])

        if invoice:
            vals.update({
                'departement_id': invoice.departement_id.id,

            })
        if statement_line and (not 'departement_id' in vals or not vals['departement_id']):
            vals.update({
                'departement_id': statement_line.departement_id.id,

            })
        res = super(AccountMoveLine, self).create(vals)

        return res
