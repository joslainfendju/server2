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
        #chargement des paramètres
        parametre_bloquer_limite_credit=self.env['ir.config_parameter'].search([('key', '=', 'BLOCK_CREDIT_LIMIT_ON_CUSTOMER')])
        parametre_bloquer_facture_echue=self.env['ir.config_parameter'].search([('key', '=', 'BLOCK_CUSTOMER_WITH_OVERDUE_INVOICES')])
        
        partner = self.partner_id
        today_dt = datetime.strftime(datetime.now().date(), DF)


        #cas de blocage des clients ayant dépassés leurs limites de crédits
        if(parametre_bloquer_limite_credit.value=='True'):
            domain = [('partner_id', '=', self.partner_id.id),
                      ('state', '=', 'progress')]

            order_lines = self.env['sale.order'].search(domain)
            
            none_invoiced_amount = sum(order_lines.mapped('amount_total'))

            
            

            available_credit = self.partner_id.credit_limit-self.partner_id.credit-none_invoiced_amount

            if self.amount_total > available_credit:
                if not partner.over_credit:
                    msg = 'Can not confirm Sale Order,Total mature due Amount ' \
                          '%s as on %s !\nCheck Partner Accounts or Credit ' \
                          'Limits !' % (available_credit , today_dt)
                    raise UserError(_('Credit Over Limits !\n' + msg))
                #partner.write({'credit_limit': credit - debit + self.amount_total})

            if(parametre_bloquer_facture_echue.value=='True'):
                invoices=self.env['account.invoice'].search(['&',('state', 'not in', ['draft', 'cancel','paid']),'&',('type','in', ('out_invoice', 'out_refund')),('partner_id','=',partner.id)])
                for invoice in invoices:
                    if(invoice.date_due and invoice.date_due<today_dt):
                        msg = 'Can not confirm Sale Order,the settlement date of an invoice  have exceeded' \
                          ' on the %s !' % (invoice.date_due)
                        raise UserError(_('Payment Overdue !\n' + msg))
        return True

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.check_limit()
        return res