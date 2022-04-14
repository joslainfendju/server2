# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: fasluca(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_tax = sum(line.amount_total for line in self.tax_line_ids)

        # self.amount_total = self.amount_untaxed + self.amount_tax
        # self.amount_discount = sum((line.quantity * line.price_unit * line.discount)/100 for line in self.invoice_line_ids)
        self.amount_discount = sum((line.quantity * line.price_unit * line.discount)/100 for line in self.invoice_line_ids)
        self.amount_total = self.amount_untaxed - self.amount_discount

        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], string='Discount Type',
                                     readonly=True, states={'draft': [('readonly', False)]}, default='percent')
    discount_rate = fields.Float('Discount Amount', digits=(16, 2), readonly=True, states={'draft': [('readonly', False)]})
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_compute_amount',
                                      track_visibility='always')

    @api.onchange('discount_type', 'discount_rate', 'invoice_line_ids')
    def supply_rate(self):
        for inv in self:
            if inv.discount_type == 'percent':
                for line in inv.invoice_line_ids:
                    line.discount = inv.discount_rate
            else:
                total = discount = 0.0
                for line in inv.invoice_line_ids:
                    total += (line.quantity * line.price_unit)
                if inv.discount_rate != 0:
                    discount = (inv.discount_rate / total) * 100
                else:
                    discount = inv.discount_rate
                for line in inv.invoice_line_ids:
                    line.discount = discount

    @api.multi
    def compute_invoice_totals(self, company_currency, invoice_move_lines):
        total = 0
        total_currency = 0
        for line in invoice_move_lines:
            if self.currency_id != company_currency:
                currency = self.currency_id.with_context(date=self.date or self.date_invoice or fields.Date.context_today(self))
                line['currency_id'] = currency.id
                line['amount_currency'] = currency.round(line['price'])
                line['price'] = currency.compute(line['price'], company_currency)
            else:
                line['currency_id'] = False
                line['amount_currency'] = False
                line['price'] = line['price']
            if self.type in ('out_invoice', 'in_refund'):
                total += line['price']
                total_currency += line['amount_currency'] or line['price']
                line['price'] = - line['price']
            else:
                total -= line['price']
                total_currency -= line['amount_currency'] or line['price']
        return total, total_currency, invoice_move_lines

    @api.multi
    def button_dummy(self):
        self.supply_rate()
        return True


    #Méthode à redéfinir pour modifier Amount Due

    # @api.one
    # @api.depends(
    #     'state', 'currency_id', 'invoice_line_ids.price_subtotal',
    #     'move_id.line_ids.amount_residual',
    #     'move_id.line_ids.currency_id')
    # def _compute_residual(self):
    #     residual = 0.0
    #     residual_company_signed = 0.0
    #     sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
    #     for line in self.sudo().move_id.line_ids:
    #         if line.account_id == self.account_id:
    #             residual_company_signed += line.amount_residual
    #             if line.currency_id == self.currency_id:
    #                 residual += line.amount_residual_currency if line.currency_id else line.amount_residual
    #             else:
    #                 from_currency = (line.currency_id and line.currency_id.with_context(date=line.date)) or line.company_id.currency_id.with_context(date=line.date)
    #                 residual += from_currency.compute(line.amount_residual, self.currency_id)
    #     self.residual_company_signed = abs(residual_company_signed) * sign
    #     self.residual_signed = abs(residual) * sign
    #     self.residual = abs(residual)
    #     digits_rounding_precision = self.currency_id.rounding
    #     if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
    #         self.reconciled = True
    #     else:
    #         self.reconciled = False

    #fin

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    discount = fields.Float(string='Discount (%)', digits=(16, 20), default=0.0)

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        #price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        price = self.price_unit
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.with_context(date=self.invoice_id._get_currency_rate_date()).compute(price_subtotal_signed, self.invoice_id.company_id.currency_id)
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign