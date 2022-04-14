# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from datetime import datetime, timedelta
from odoo.addons.web.controllers.main import clean_action
from odoo.tools import float_is_zero

class report_account_general_ledger(models.AbstractModel):

    _inherit = "account.general.ledger"


    def get_columns_name(self, options):
        res = super(report_account_general_ledger, self).get_columns_name(options)
        res.insert(2, {'name': _("Voucher Type")})
        return res

    @api.model
    def get_lines(self, options, line_id=None):
        lines = []
        context = self.env.context
        company_id = self.env.user.company_id
        dt_from = options['date'].get('date_from')
        line_id = line_id and int(line_id.split('_')[1]) or None
        aml_lines = []
        # Aml go back to the beginning of the user chosen range but the amount on the account line should go back
        # to either the beginning of the fy or the beginning of times depending on the account
        grouped_accounts = self.with_context(date_from_aml=dt_from, date_from=dt_from and
                                                                              company_id.compute_fiscalyear_dates(
                                                                                  datetime.strptime(dt_from,
                                                                                                    "%Y-%m-%d"))[
                                                                                  'date_from'] or None).group_by_account_id(
            options, line_id)
        sorted_accounts = sorted(grouped_accounts, key=lambda a: a.code)
        unfold_all = context.get('print_mode') and len(options.get('unfolded_lines')) == 0
        for account in sorted_accounts:
            debit = grouped_accounts[account]['debit']
            credit = grouped_accounts[account]['credit']
            balance = grouped_accounts[account]['balance']
            amount_currency = '' if not account.currency_id else self.format_value(
                grouped_accounts[account]['amount_currency'], currency=account.currency_id)
            lines.append({
                'id': 'account_%s' % (account.id,),
                'name': account.code + " " + account.name,
                'columns': [{'name': v} for v in ['', amount_currency, self.format_value(debit), self.format_value(credit),
                                                  self.format_value(balance)]],
                'level': 2,
                'unfoldable': True,
                'unfolded': 'account_%s' % (account.id,) in options.get('unfolded_lines') or unfold_all,
                'colspan': 4,
            })
            if 'account_%s' % (account.id,) in options.get('unfolded_lines') or unfold_all:
                initial_debit = grouped_accounts[account]['initial_bal']['debit']
                initial_credit = grouped_accounts[account]['initial_bal']['credit']
                initial_balance = grouped_accounts[account]['initial_bal']['balance']
                initial_currency = '' if not account.currency_id else self.format_value(
                    grouped_accounts[account]['initial_bal']['amount_currency'], currency=account.currency_id)
                domain_lines = [{
                    'id': 'initial_%s' % (account.id,),
                    'class': 'o_account_reports_initial_balance',
                    'name': _('Initial Balance'),
                    'parent_id': 'account_%s' % (account.id,),
                    'columns': [{'name': v} for v in ['', '', '', '', initial_currency, self.format_value(initial_debit),
                                                      self.format_value(initial_credit),
                                                      self.format_value(initial_balance)]],
                }]
                progress = initial_balance
                amls = amls_all = grouped_accounts[account]['lines']
                too_many = False
                if len(amls) > 80 and not context.get('print_mode'):
                    amls = amls[:80]
                    too_many = True
                used_currency = self.env.user.company_id.currency_id
                for line in amls:
                    if options.get('cash_basis'):
                        line_debit = line.debit_cash_basis
                        line_credit = line.credit_cash_basis
                    else:
                        line_debit = line.debit
                        line_credit = line.credit
                    line_debit = line.company_id.currency_id.compute(line_debit, used_currency)
                    line_credit = line.company_id.currency_id.compute(line_credit, used_currency)
                    progress = progress + line_debit - line_credit
                    currency = "" if not line.currency_id else self.with_context(no_format=False).format_value(
                        line.amount_currency, currency=line.currency_id)
                    name = []
                    name = line.name and line.name or ''
                    if line.ref:
                        name = name and name + ' - ' + line.ref or line.ref
                    if len(name) > 35 and not self.env.context.get('no_format'):
                        name = name[:32] + "..."
                    partner_name = line.partner_id.name
                    if partner_name and len(partner_name) > 35 and not self.env.context.get('no_format'):
                        partner_name = partner_name[:32] + "..."
                    caret_type = 'account.move'
                    if line.invoice_id:
                        caret_type = 'account.invoice.in' if line.invoice_id.type in (
                        'in_refund', 'in_invoice') else 'account.invoice.out'
                    elif line.payment_id:
                        caret_type = 'account.payment'

                    voucher_type = \
                       line.voucher_type or ''
                    line_value = {
                        'id': line.id,
                        'caret_options': caret_type,
                        'parent_id': 'account_%s' % (account.id,),
                        'name': line.move_id.name if line.move_id.name else '/',
                        'columns': [{'name': v} for v in
                                    [format_date(self.env, line.date),voucher_type, name, partner_name, currency,
                                     line_debit != 0 and self.format_value(line_debit) or '',
                                     line_credit != 0 and self.format_value(line_credit) or '',
                                     self.format_value(progress)]],
                        'level': 4,
                    }
                    aml_lines.append(line.id)
                    domain_lines.append(line_value)
                domain_lines.append({
                    'id': 'total_' + str(account.id),
                    'class': 'o_account_reports_domain_total',
                    'parent_id': 'account_%s' % (account.id,),
                    'name': _('Total '),
                    'columns': [{'name': v} for v in
                                ['', '', '', '', amount_currency, self.format_value(debit), self.format_value(credit),
                                 self.format_value(balance)]],
                })
                if too_many:
                    domain_lines.append({
                        'id': 'too_many' + str(account.id),
                        'parent_id': 'account_%s' % (account.id,),
                        'name': _('There are more than 80 items in this list, click here to see all of them'),
                        'colspan': 7,
                        'columns': [{}],
                        'action': 'view_too_many',
                        'action_id': 'account,%s' % (account.id,),
                    })
                lines += domain_lines

        journals = [j for j in options.get('journals') if j.get('selected')]
        if len(journals) == 1 and journals[0].get('type') in ['sale', 'purchase'] and not line_id:
            total = self._get_journal_total()
            lines.append({
                'id': 0,
                'class': 'total',
                'name': _('Total'),
                'columns': [{'name': v} for v in
                            ['', '', '', '', self.format_value(total['debit']), self.format_value(total['credit']),
                             self.format_value(total['balance'])]],
                'level': 1,
                'unfoldable': False,
                'unfolded': False,
            })
            lines.append({
                'id': 0,
                'name': _('Tax Declaration'),
                'columns': [{'name': v} for v in ['', '', '', '', '', '', '']],
                'level': 1,
                'unfoldable': False,
                'unfolded': False,
            })
            lines.append({
                'id': 0,
                'name': _('Name'),
                'columns': [{'name': v} for v in ['', '', '', '', _('Base Amount'), _('Tax Amount'), '']],
                'level': 2,
                'unfoldable': False,
                'unfolded': False,
            })
            for tax, values in self._get_taxes(journals[0]).items():
                lines.append({
                    'id': '%s_tax' % (tax.id,),
                    'name': tax.name + ' (' + str(tax.amount) + ')',
                    'caret_options': 'account.tax',
                    'unfoldable': False,
                    'columns': [{'name': v} for v in ['', '', '', '', values['base_amount'], values['tax_amount'], '']],
                    'level': 4,
                })

        if self.env.context.get('aml_only', False):
            return aml_lines
        return lines


