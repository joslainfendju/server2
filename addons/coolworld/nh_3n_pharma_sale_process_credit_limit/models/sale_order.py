# See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def check_limit(self):
        self.ensure_one()
        # chargement des paramètres
        parametre_bloquer_limite_credit = self.env['ir.config_parameter'].search(
            [('key', '=', 'BLOCK_CREDIT_LIMIT_ON_CUSTOMER')])
        parametre_bloquer_facture_echue = self.env['ir.config_parameter'].search(
            [('key', '=', 'BLOCK_CUSTOMER_WITH_OVERDUE_INVOICES')])

        partner = self.partner_id
        today_dt = datetime.strftime(datetime.now().date(), DF)

        # cas de blocage des clients ayant dépassés leurs limites de crédits
        if (parametre_bloquer_limite_credit.value == 'True'):
            domain = [('partner_id', '=', self.partner_id.id),
                      ('state', '=', 'progress')]

            order_lines = self.env['sale.order'].search(domain)

            none_invoiced_amount = sum(order_lines.mapped('amount_total'))

            available_credit = self.partner_id.credit_limit - self.partner_id.credit - none_invoiced_amount

            state_msg = self.env.ref('nh_3n_pharma_sale_process_credit_limit.balance').value + str(
                partner.credit) + "\n" + \
                        self.env.ref('nh_3n_pharma_sale_process_credit_limit.credit_limit').value + str(
                partner.credit_limit) + "\n" + \
                        self.env.ref('nh_3n_pharma_sale_process_credit_limit.available_credit').value + str(
                available_credit)

            if self.amount_total > available_credit:

                if not partner.over_credit:

                    msg = self.env.ref('nh_3n_pharma_sale_process_credit_limit.cash_message_header').value
                    if partner.customer_type == 'credit':
                        msg = self.env.ref('nh_3n_pharma_sale_process_credit_limit.credit_message_header').value

                    raise UserError(_(msg+ "\n" + state_msg))

            if (parametre_bloquer_facture_echue.value == 'True'):
                invoices = self.env['account.invoice'].search(
                    ['&', ('state', 'not in', ['draft', 'cancel', 'paid']), '&',
                     ('type', 'in', ('out_invoice', 'out_refund')), ('partner_id', '=', partner.id)])
                for invoice in invoices:
                    if (invoice.date_due and invoice.date_due < today_dt):
                        msg =   self.env.ref('nh_3n_pharma_sale_process_credit_limit.date_due_message_header').value + str(invoice.date_due)

                        raise UserError(_(msg+"\n"+ state_msg ))
        return True

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.check_limit()
        return res

    @api.multi
    def action_sale_head_validation(self):
        if self.check_limit():
          super(SaleOrder, self).action_sale_head_validation()