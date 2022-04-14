from odoo import models, fields, api,_
import logging
from datetime import datetime , timedelta
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

_customer_account_prefix="411"
_cash_account_prefix="57"
_bank_account_prefix="52"


class Branch(models.Model):
    _inherit = "res.branch"
    _name = 'res.branch'


    sale_amount_total = fields.Float(compute="_get_sale_total_month", string = "Sale  Amount Total")
    collect_amount_month = fields.Float(compute="_get_collect_amount_month", string = "Collect  Amount of Month")

    @api.one
    def _get_sale_amount_total(self):
        sales = self.env['sale.order'].search(['&',('branch_id','=', self.id),('state','in', ('sale','done',))])
        currency_id = self.env.user.company_id.currency_id

        self.sale_amount_total = 0.0
        for sale in sales :
            self.sale_amount_total +=  sale.currency_id.compute(sale.amount_total , currency_id,False)

    @api.one
    def _get_sale_total_month(self):
        currency_id = self.env.user.company_id.currency_id

        dt = datetime.now()
        start_string = dt.strftime('%Y-%m') + '-01 00:00:00'
        end_string = dt.strftime('%Y-%m-%d %H:%M:%S')

        sales = self.env['sale.order'].search(
            ['&',('branch_id','=', self.id),'&', ('state', 'in', ('sale', 'done',)), '&', ('date_order', '>=', start_string),
             ('date_order', '<=', end_string), ])
        self.sale_amount_total = 0.0
        for sale in sales:
            self.sale_amount_total += sale.currency_id.compute(sale.amount_total, currency_id, False)

    @api.one
    def _get_collect_amount_month(self):
        dt = datetime.now()
        start_string = dt.strftime('%Y-%m') + '-01 00:00:00'
        end_string = dt.strftime('%Y-%m-%d %H:%M:%S')

        self.collect_amount_month = self._get_collect_amount(self, start_string, end_string)

    @api.one
    def get_transit_move_lines(self):
        date_format = "%Y-%m-%d %H:%M:%S"

        specific_date = datetime.datetime.strptime(fields.Datetime.now(), date_format).replace(hour=0, minute=0,
                                                                                               second=0,
                                                                                               microsecond=0)
        specific_date = specific_date.strftime('%Y-%m-%d') + ' 23:59:59'
        base_domain = []
        en_transit_domain = ['&', ('picking_id', '!=', False), '&', '!',
                             ('picking_id.state', 'in', ('done', 'cancel',)),
                             '&', '|', ('picking_id.receipt_from_request_id', '!=', False),
                             ('picking_id.receipt_from_return_request_id', '!=', False),
                             ('date', '<=', specific_date)
                             ]

        base_domain = en_transit_domain

        logging.info("domaine transit dans stock real transit report est " + str(base_domain))

        return self.env['stock.move'].search(base_domain, order='branch_id')


    def _get_collect_amount(self, branch_id ,start_date,end_date):
        obj_acj = self.env['account.journal']
        journals = obj_acj.search([('type', 'in', ['cash', 'bank'])])
        total_debit = 0.0
        total_credit = 0.0

        for j in journals:
            for mv in self.env['account.move'].search(
                    [('journal_id', '=', j.id), ('date', '>=', start_date), ('date', '<=', end_date),
                     ('state', '=', 'posted'), ('branch_id', '=', branch_id.id)]):

                l1 = mv.line_ids[0]
                l2 = mv.line_ids[1]
                if l1.account_id.code.startswith(_cash_account_prefix) and l2.account_id.code.startswith(
                        _customer_account_prefix) or l1.account_id.code.startswith(
                        _bank_account_prefix) and l2.account_id.code.startswith(_customer_account_prefix):
                    if l2.credit != 0:
                        total_credit += l2.credit
                    elif l2.debit != 0:
                        total_debit += l2.debit

        collect_amount = total_credit-total_debit

        return collect_amount


