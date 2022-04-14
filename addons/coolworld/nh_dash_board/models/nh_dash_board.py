# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

from babel.dates import format_datetime, format_date
from datetime import datetime , timedelta

from odoo import models, api, _, fields
from odoo.release import version
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools.misc import formatLang

from odoo import models, fields, api


import logging

_customer_account_prefix="411"
_cash_account_prefix="57"
_bank_account_prefix="52"



class CustomSalesDashboard(models.Model):
    _name = "nh.dashboard"

    """
        This is meta data for manage various dashboard
    """
    color = fields.Integer(string='Color Index')
    name = fields.Char(string="Name")
    application = fields.Selection([('sale', 'Sale'), ('purchase', 'Purchase'), ('stock_request', 'Stock Request'), ('payment', 'Payment'),('customers', 'Customers'),('stock', 'Stock')], string='Application',
                     default='sale')

    """
        The sale dashboard attribute
    """
    branch_sale_json = fields.Text(compute='_get_branch_sale_json')
    oustanding_customers_json = fields.Text(compute='_get_oustanding_customers_json')

    total_sale_weekly = fields.Float(compute = '_get_sale_total_week')
    total_sale_monthly = fields.Float(compute = '_get_sale_total_month')
    total_sale_yearly = fields.Float(compute = '_get_sale_total_year')

    count_done_sales = fields.Integer(compute='_get_count_sales')
    count_undone_sales = fields.Integer(compute='_get_count_sales')

    count_done_deliveries = fields.Integer(compute='_get_count_deliveries')
    count_undone_deliveries = fields.Integer(compute='_get_count_deliveries')

    """
        Products Dashboard attribute
    """
    products_json = fields.Text(compute='_get_products_json')
    branch_ids = fields.One2many('res.branch', compute='_get_branch_ids')

    """
        Purchase Dashboard   
    """
    count_draft_purchase = fields.Integer(compute='_get_count_purchases')
    count_confirmed_purchase = fields.Integer(compute='_get_count_purchases')
    count_production_purchase = fields.Integer(compute='_get_count_purchases')
    count_transit_purchase = fields.Integer(compute='_get_count_purchases')
    count_landed_purchase = fields.Integer(compute='_get_count_purchases')
    count_total_purchase = fields.Integer(compute='_get_count_purchases')

    count_draft_purchase_max_days = fields.Integer(compute='_get_count_purchases')
    count_confirmed_purchase_max_days = fields.Integer(compute='_get_count_purchases')
    count_production_purchase_max_days = fields.Integer(compute='_get_count_purchases')
    count_transit_purchase_max_days = fields.Integer(compute='_get_count_purchases')
    count_landed_purchase_max_days = fields.Integer(compute='_get_count_purchases')

    value_draft_purchase = fields.Float(compute='_get_count_purchases')
    value_confirmed_purchase = fields.Float(compute='_get_count_purchases')
    value_production_purchase = fields.Float(compute='_get_count_purchases')
    value_transit_purchase = fields.Float(compute='_get_count_purchases')
    value_landed_purchase = fields.Float(compute='_get_count_purchases')

    """
        Stock Request Dasboard
    """
    count_draft_request = fields.Integer(compute='_get_count_stock_requests')
    count_approved_request = fields.Integer(compute='_get_count_stock_requests')
    count_transit_request = fields.Integer(compute='_get_count_stock_requests')
    count_done_request = fields.Integer(compute='_get_count_stock_requests')
    count_total_request = fields.Integer(compute='_get_count_stock_requests')

    count_draft_request_max_days = fields.Integer(compute='_get_count_stock_requests')
    count_approved_request_max_days = fields.Integer(compute='_get_count_stock_requests')
    count_transit_request_max_days = fields.Integer(compute='_get_count_stock_requests')
    count_done_request_max_days= fields.Integer(compute='_get_count_stock_requests')
    count_total_request_max_days = fields.Integer(compute='_get_count_stock_requests')

    value_draft_request = fields.Float(compute='_get_count_stock_requests')
    value_approved_request = fields.Float(compute='_get_count_stock_requests')
    value_transit_request = fields.Float(compute='_get_count_stock_requests')
    value_done_request = fields.Float(compute='_get_count_stock_requests')


    count_done_receipt_orders = fields.Integer(compute='_get_receipt_orders')
    count_undone_receipt_orders = fields.Integer(compute='_get_receipt_orders')
    currency_id = fields.Many2one('res.currency', compute='_get_company_currency')

    """
        Collection Dashboard
    """
    branch_payment_json = fields.Text(compute='_get_branch_payment_json')
    branch_ids = fields.One2many('res.branch', compute='_get_branch_ids')

    total_collect_weekly = fields.Float(compute='_get_collect_total_week')
    total_collect_monthly = fields.Float(compute='_get_collect_total_month')
    total_collect_yearly = fields.Float(compute='_get_collect_total_year')

    count_draft_invoices = fields.Integer(compute='_get_count_invoices')
    count_open_invoices = fields.Integer(compute='_get_count_invoices')
    count_paid_invoices = fields.Integer(compute='_get_count_invoices')
    count_outstanding_customers = fields.Integer(compute='_get_count_outstanding_customers')

    @api.one
    def _get_count_sales(self):
        """if self.application != 'sale':
            return"""
        sales_done = self.env['sale.order'].search(
            [ ('state', 'in', ('sale', 'done',)) ])
        self.count_done_sales = len(sales_done)
        sales_draft = self.env['sale.order'].search(
            ['!', ('state', 'in', ('sale', 'done','cancel'))])
        self.count_undone_sales = len(sales_draft)

    @api.one
    def _get_count_invoices(self):
        """if self.application != 'payment':
            return"""
        draft = self.env['account.invoice'].search([('state', 'in', ('draft',)),('type','in',('out_invoice',))])
        open = self.env['account.invoice'].search([('state', 'in', ('open',)),('type','in',('out_invoice',))])
        paid = self.env['account.invoice'].search([('state', 'in', ('paid',)),('type','in',('out_invoice',))])

        self.count_draft_invoices = len (draft)
        self.count_open_invoices = len(open)
        self.count_paid_invoices = len (paid)



    @api.one
    def _get_count_outstanding_customers(self):
        """if self.application != 'customers':
            return"""
        customers = self.env['res.partner'].search([('customer', '=', True),('credit','>',0)])
        self.count_outstanding_customers = len(customers)


    @api.one
    def _get_count_deliveries(self):
        """if self.application != 'sale':
            return"""
        deliveries_done = self.env['stock.picking'].search(
            ['&', ('picking_type_id.code', '=', 'outgoing'), ('state', 'in', ('done',))])
        self.count_done_deliveries = len(deliveries_done)
        deliveries_draft = self.env['stock.picking'].search(
            ['&', ('picking_type_id.code', '=', 'outgoing'), '!', ('state', 'in', ('done', 'cancel',))])
        self.count_undone_deliveries = len(deliveries_draft)

    @api.one
    def _get_receipt_orders(self):
        """if self.application != 'purchase':
            return"""
        receipts_done = self.env['stock.picking'].search(
            ['&', ('picking_type_id.code', '=', 'incoming'), ('state', 'in', ('done',))])
        self.count_done_receipt_orders = len(receipts_done)
        receipts_draft = self.env['stock.picking'].search(
            ['&', ('picking_type_id.code', '=', 'incoming'), '!', ('state', 'in', ('done', 'cancel',))])
        self.count_undone_receipt_orders = len(receipts_draft)

    @api.one
    def _get_count_purchases(self):
        """if self.application != 'purchase':
            return"""
        purchase_abroad = self.env['purchase.order'].search(['&',('type','=','abroad'),'!',('state', 'in', ('cancel', ))])
        purchase_draft = self.env['purchase.order'].search(['&',('type','=','abroad'),('state', 'in', ('draft', ))] , order='date_order ASC')
        purchase_confirmed = self.env['purchase.order'].search(['&',('type','=','abroad'),('state', 'in', ('purchase', ))] , order='date_confirm ASC')
        purchase_prodution = self.env['purchase.order'].search(['&',('type','=','abroad'),('state', 'in', ('production', ))] , order='date_production_start ASC')
        purchase_transit = self.env['purchase.order'].search(['&',('type','=','abroad'),('state', 'in', ('transit', ))] , order='date_transit ASC')
        purchase_landed = self.env['purchase.order'].search(['&',('type','=','abroad'),('state', 'in', ('landed', ))], order='date_arrival ASC')

        self.count_draft_purchase = len(purchase_draft)
        self.count_confirmed_purchase = len(purchase_confirmed)
        self.count_production_purchase = len (purchase_prodution)
        self.count_transit_purchase = len(purchase_transit)
        self.count_landed_purchase = len (purchase_landed)
        self.count_total_purchase = len (purchase_abroad)

        date_format = "%Y-%m-%d %H:%M:%S"
        simple_date_format = "%Y-%m-%d"
        maintenant = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        self.value_draft_purchase = self.get_total_purchase(self.currency_id,purchase_draft)
        self.value_purchase_confirmed = self.get_total_purchase(self.currency_id,purchase_confirmed)
        self.value_purchase_prodution = self.get_total_purchase(self.currency_id,purchase_prodution)
        self.value_transit_purchase = self.get_total_purchase(self.currency_id,purchase_transit)
        self.value_landed_purchase = self.get_total_purchase(self.currency_id,purchase_landed)

        if (purchase_draft):
            dateDebut = datetime.strptime(purchase_draft[0].date_order, date_format).replace(hour=0, minute=0,second=0, microsecond=0)
            self.count_draft_purchase_max_days = (maintenant - dateDebut).total_seconds() / 86400

        if (purchase_confirmed):
            #dateDebut = datetime.strptime(purchase_confirmed[0].date_confirm, date_format).replace(hour=0, minute=0,second=0, microsecond=0)
            dateDebut = datetime.strptime(purchase_confirmed[0].date_confirm, simple_date_format)
            self.count_confirmed_purchase_max_days = (maintenant - dateDebut).total_seconds() / 86400

        if (purchase_prodution):
            dateDebut = datetime.strptime(purchase_prodution[0].date_production_start+' 00:00:00', date_format)
            self.count_production_purchase_max_days = (maintenant - dateDebut).total_seconds() / 86400

        if (purchase_transit):
            dateDebut = datetime.strptime(purchase_transit[0].date_transit+' 00:00:00', date_format)
            self.count_transit_purchase_max_days= (maintenant - dateDebut).total_seconds() / 86400

        if (purchase_landed):
            dateDebut = datetime.strptime(purchase_landed[0].date_arrival+' 00:00:00', date_format)
            self.count_landed_purchase_max_days= (maintenant - dateDebut).total_seconds() / 86400

    @api.one
    def _get_stock_requests_by_state(self):
        date_format = "%Y-%m-%d %H:%M:%S"
        requests = self.env['nh_scm.stock_request'].search([('id', '>', 0)])
        request_draft = self.env['nh_scm.stock_request'].search([('state', 'in', ('draft',))], order='request_date ASC')
        request_approved = [request for request in self.env['nh_scm.stock_request'].search([('state', 'in', ('approved',))],
                                                                   order='approved_date ASC')]
        request_transit = [request for request in self.env['nh_scm.stock_request'].search([('state', 'in', ('transit',))],
                                                                  order='transit_date ASC')]
        request_partially_transit = self.env['nh_scm.stock_request'].search([('state', 'in', ('partially_transit',))],
                                                                  order='transit_date ASC')
        request_done = self.env['nh_scm.stock_request'].search([('state', 'in', ('done', 'locked',))])

        for request in request_partially_transit:
            is_just_approved = True
            for transfer in request.receipt_picking_ids:
                if transfer.state not in ('done', 'cancel' ):
                    is_just_approved = False
                    request_transit.append(request)
                    break
            if is_just_approved:
                request_approved.append(request)

        request_approved.sort(key=lambda r: datetime.strptime(r.approved_date, date_format)
                                        .replace(hour=0, minute=0, second=0, microsecond=0))
        request_transit.sort(key=lambda r: datetime.strptime(r.transit_date, date_format)
                                        .replace(hour=0, minute=0, second=0, microsecond=0))
        return requests, request_draft, request_approved, request_transit, request_done



    @api.one
    def _get_count_stock_requests(self):
        """if self.application != 'stock_request':
            return"""
        date_format = "%Y-%m-%d %H:%M:%S"
        maintenant = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        requests, request_draft, request_approved, request_transit, request_done = \
            self._get_stock_requests_by_state()[0]

        self.count_draft_request = len(request_draft)
        self.count_transit_request = len(request_transit)
        self.count_approved_request = len(request_approved)
        self.count_done_request = len(request_done)
        self.count_total_request = len(requests)

        if request_draft:
            dateDebut = datetime.strptime(request_draft[0].request_date, date_format).replace(hour=0, minute=0,second=0,microsecond=0)
            self.count_draft_request_max_days = (maintenant -dateDebut).total_seconds() / 86400
        if request_approved:
            dateDebut = datetime.strptime(request_approved[0].approved_date, date_format).replace(hour=0, minute=0,second=0,microsecond=0)
            self.count_approved_request_max_days = (maintenant-dateDebut).total_seconds() / 86400
        if request_transit and request_transit[0].transit_date:
            dateDebut = datetime.strptime(request_transit[0].transit_date, date_format).replace(hour=0, minute=0,second=0,microsecond=0)
            self.count_transit_request_max_days = (maintenant-dateDebut).total_seconds() / 86400

        self.value_draft_request = self.get_total_stock_request(self.currency_id, request_draft)
        self.value_approved_request = self.get_total_stock_request(self.currency_id, request_approved)
        self.value_transit_request = self.get_total_stock_request(self.currency_id, request_transit)
        self.value_done_request = self.get_total_stock_request(self.currency_id, request_done)

    @api.one
    def _get_company_currency(self):
       self.currency_id =  self.env.user.company_id.currency_id

    @api.one
    def _get_sale_total_week(self):
        """if self.application != 'sale':
            return"""

        dt = datetime.now ()
        start_week = dt - timedelta(days=dt.weekday())
        end_week = start_week + timedelta(days=6)

        start_week_string = start_week.strftime('%Y-%m-%d') +' 00:00:00'
        end_week_string =  end_week.strftime('%Y-%m-%d') +' 23:59:59'

        sales = self.env['sale.order'].search(['&', ('state', 'in', ('sale', 'done',)),'&',('date_order', '>=', start_week_string), ('date_order', '<=', end_week_string), ])

        self.total_sale_weekly = 0.0
        for sale in sales:
            self.total_sale_weekly += sale.currency_id.compute(sale.amount_total , self.currency_id,False)


    def get_total_purchase(self,currency_id,purchases):
        """if self.application != 'purchase':
            return"""
        total = 0.0
        for purchase in purchases:
            total += purchase.currency_id.compute(purchase.amount_total , currency_id,False)
        return  total

    def get_total_stock_request(self,currency_id,requests):
        """if self.application != 'stock_request':
            return"""
        total = 0.0
        for request in requests:
            total += request.currency_id.compute(request.total_price , currency_id,False)
        return  total


    @api.one
    def _get_sale_total_month(self):
        """if self.application != 'sale':
            return"""
        dt = datetime.now()
        start_string = dt.strftime('%Y-%m')+'-01 00:00:00'
        end_string = dt.strftime('%Y-%m-%d %H:%M:%S')

        sales = self.env['sale.order'].search(
            ['&', ('state', 'in', ('sale', 'done',)),'&', ('date_order', '>=', start_string),
             ('date_order', '<=', end_string), ])
        self.total_sale_monthly = 0.0
        for sale in sales:
            self.total_sale_monthly += sale.currency_id.compute(sale.amount_total , self.currency_id,False)

    @api.one
    def _get_sale_total_year(self):
        """if self.application != 'sale':
            return"""
        dt = datetime.now()
        start_string = dt.strftime('%Y') + '-01-01 00:00:00'
        end_string = dt.strftime('%Y-%m-%d %H:%M:%S')

        sales = self.env['sale.order'].search(
            ['&', ('state', 'in', ('sale', 'done',)),'&', ('date_order', '>=', start_string),
             ('date_order', '<=', end_string), ])
        self.total_sale_yearly = 0.0
        for sale in sales:
            self.total_sale_yearly += sale.currency_id.compute(sale.amount_total , self.currency_id,False)

    @api.one
    def _get_branch_payment_json(self):
        """if self.application != 'payment':
            return"""
        data = []
        branches = self.env['res.branch'].search([('id', '>', 0)])
        for branch in branches:
            dict = {'label':branch.name,'value': branch.collect_amount_month}
            data.append(dict)

        self.branch_payment_json = json.dumps(data)

    @api.one
    def _get_branch_sale_json(self):
        """if self.application != 'sale':
            return"""
        data = []
        branches = self.env['res.branch'].search([('id', '>', 0)])
        for branch in branches:
            # dict = {'label':branch.name,'value': branch.collect_amount_month}
            dict = {'label': branch.name, 'value':  branch.sale_amount_total}

            data.append(dict)

        # self.branch_payment_json = str(data)
        self.branch_sale_json = json.dumps(data)

    @api.one
    def _get_oustanding_customers_json(self):
        """if self.application != 'customers':
            return"""
        data = []
        customers = self.env['res.partner'].search([('customer', '=', True),('credit','>',0)],limit=10)
        for customer in customers:
            # dict = {'label':branch.name,'value': branch.collect_amount_month}
            dict = {'label': customer.display_name, 'value': customer.credit}

            data.append(dict)

        # self.branch_payment_json = str(data)
        self.oustanding_customers_json = json.dumps(data)

    @api.one
    def _get_products_json(self):
        """if self.application != 'stock':
            return"""
        data = []

        products = self.env['product.product'].search([('product_tmpl_id.type', '=', 'product')])
        tab =  []
        for product in products:
            tab.append(product)
        tab.sort(key=lambda x: x.with_context({'product_uom' : x.product_tmpl_id.uom_id.id}).qty_available*x.standard_price , reverse=True)
        max=20
        for product in tab:
            max -=1
            product_val = product.with_context({'product_uom' : product.product_tmpl_id.uom_id.id}).qty_available * product.standard_price
            if product_val <= 0:
                break
            # dict = {'label':branch.name,'value': branch.collect_amount_month}
            dict = {'label': product.product_tmpl_id.default_code, 'value': product_val}
            data.append(dict)
            if max ==0 :
                break

        # self.branch_payment_json = str(data)
        self.products_json = json.dumps(data)

    @api.multi
    def action_open_outstanding_customers(self):
        """return action based on type for related action"""

        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'customers':
                action_name = 'action_partner_form'
        ctx = self._context.copy()
        ctx.update({
            # 'group_by': ['branch_id', 'date_order']

        })

        [action] = self.env.ref('base.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [('customer', '=', True), ('credit', '>', 0)])

        return action

    @api.multi
    def action_open_products(self):
        """return action based on type for related action"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'stock':
                action_name = 'product_template_action_all'
        ctx = self._context.copy()
        ctx.update({
            #'group_by': ['branch_id', 'date_order']

        })

        [action] = self.env.ref('product.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [ ('type', 'in', ('product',)) ])

        return action

    @api.one
    def _get_branch_ids(self):
        self.branch_ids = self.env['res.branch'].search([('id', '>', 0)])

    @api.multi
    def action_open_montly_sales(self):
        """return action based on type for related action"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'sale':
                action_name = 'action_orders'
        dt = datetime.now()
        start_string = dt.strftime('%Y-%m') + '-01 00:00:00'
        end_string = dt.strftime('%Y-%m-%d %H:%M:%S')

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id','date_order']

        })

        [action] = self.env.ref('sale.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&', ('state', 'in', ('sale', 'done',)), '&',
                                                            ('date_order', '>=', start_string),
                                                            ('date_order', '<=', end_string), ])
        sale_filter = self.env.ref('sale.view_sales_order_filter', False)
        action['search_view_id'] = sale_filter.id

        return action

    @api.multi
    def action_open_yearly_sales(self):
        """return action based on type for related action"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'sale':
                action_name = 'action_orders'

        dt = datetime.now()
        start_string = dt.strftime('%Y-%m') + '-01 00:00:00'
        end_string = dt.strftime('%Y-%m-%d %H:%M:%S')
        start_string = dt.strftime('%Y') + '-01-01 00:00:00'
        end_string = dt.strftime('%Y-%m-%d %H:%M:%S')
        ctx = self._context.copy()
        ctx.update({
            'group_by': ['date_order','branch_id']

        })

        [action] = self.env.ref('sale.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&', ('state', 'in', ('sale', 'done',)), '&', ('date_order', '>=', start_string),
             ('date_order', '<=', end_string), ])
        sale_filter = self.env.ref('sale.view_sales_order_filter', False)
        action['search_view_id'] = sale_filter.id

        return action

    @api.multi
    def action_open_weekly_sales(self):
        """return action based on type for related action"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'sale':
                action_name = 'action_orders'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id']

        })
        dt = datetime.now()
        start_week = dt - timedelta(days=dt.weekday())
        end_week = start_week + timedelta(days=6)

        start_week_string = start_week.strftime('%Y-%m-%d') + ' 00:00:00'
        end_week_string = end_week.strftime('%Y-%m-%d') + ' 23:59:59'

        [action] = self.env.ref('sale.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&', ('state', 'in', ('sale', 'done',)),'&',
                                                            ('date_order', '>=', start_week_string),
                                                            ('date_order', '<=', end_week_string), ])
        sale_filter = self.env.ref('sale.view_sales_order_filter', False)
        action['search_view_id'] = sale_filter.id


        return action

    @api.multi
    def action_open_undone_sales(self):
        """return action based on type for related action"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'sale':
                action_name = 'action_orders'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id']

        })


        [action] = self.env.ref('sale.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['!', ('state', 'in', ('sale', 'done','cancel',))])
        sale_filter = self.env.ref('sale.view_sales_order_filter', False)
        action['search_view_id'] = sale_filter.id

        return action



    @api.multi
    def action_open_done_sales(self):
        """return action based on type for related action"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'sale':
                action_name = 'action_orders'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id']

        })

        [action] = self.env.ref('sale.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [('state', 'in', ('sale', 'done',))])
        sale_filter = self.env.ref('sale.view_sales_order_filter', False)
        action['search_view_id'] = sale_filter.id

        return action

    @api.multi
    def action_open_done_deliveries(self):
        """return action based on type for related action"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'sale':
                action_name = 'action_picking_tree_all'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id']

        })

        [action] = self.env.ref('stock.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [ '&',('picking_type_id.code','=', 'outgoing'),('state', 'in', ('done',))])
        sale_filter = self.env.ref('stock.view_picking_internal_search', False)
        action['search_view_id'] = sale_filter.id

        return action

    @api.multi
    def action_open_undone_deliveries(self):
        """return action based on type for related action"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'sale':
                action_name = 'action_picking_tree_all'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id']

        })

        [action] = self.env.ref('stock.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&',('picking_type_id.code','=', 'outgoing'),'!', ('state', 'in', ( 'done', 'cancel',))])
        sale_filter = self.env.ref('stock.view_picking_internal_search', False)
        action['search_view_id'] = sale_filter.id

        return action

    @api.multi
    def action_open_draft_purchase(self):

        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'purchase':
                action_name = 'purchase_rfq'



        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id', 'date_order']

        })

        [action] = self.env.ref('purchase.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&', ('state', 'in', ('draft',)),
                                                            ('type', '=','abroad')
                                                            ])
        purchase_filter = self.env.ref('purchase.view_purchase_order_filter', False)
        action['search_view_id'] = purchase_filter.id

        return action

    @api.multi
    def action_open_confirmed_purchase(self):

        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'purchase':
                action_name = 'purchase_rfq'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id', 'date_order']

        })

        [action] = self.env.ref('purchase.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&', ('state', 'in', ('purchase',)),
                                                            ('type', '=', 'abroad')
                                                            ])
        purchase_filter = self.env.ref('purchase.view_purchase_order_filter', False)
        action['search_view_id'] = purchase_filter.id

        return action

    @api.multi
    def action_open_production_purchase(self):

        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'purchase':
                action_name = 'purchase_rfq'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id', 'date_order']

        })

        [action] = self.env.ref('purchase.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&', ('state', 'in', ('production',)),
                                                            ('type', '=', 'abroad')
                                                            ])
        purchase_filter = self.env.ref('purchase.view_purchase_order_filter', False)
        action['search_view_id'] = purchase_filter.id

        return action

    @api.multi
    def action_open_landed_purchase(self):

        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'purchase':
                action_name = 'purchase_rfq'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id', 'date_order']

        })

        [action] = self.env.ref('purchase.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&', ('state', 'in', ('landed',)),
                                                            ('type', '=', 'abroad')
                                                            ])
        purchase_filter = self.env.ref('purchase.view_purchase_order_filter', False)
        action['search_view_id'] = purchase_filter.id

        return action

    @api.multi
    def action_open_transit_purchase(self):

        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'purchase':
                action_name = 'purchase_rfq'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id', 'date_order']

        })

        [action] = self.env.ref('purchase.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&', ('state', 'in', ('transit',)),
                                                            ('type', '=', 'abroad')
                                                            ])
        purchase_filter = self.env.ref('purchase.view_purchase_order_filter', False)
        action['search_view_id'] = purchase_filter.id

        return action

    @api.multi
    def action_open_done_receipt_orders(self):
        """return action based on type for related action"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'purchase':
                action_name = 'action_picking_tree_all'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id']

        })

        [action] = self.env.ref('stock.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&', ('picking_type_id.code', '=', 'incoming'),
                                                            ('state', 'in', ('done',))])
        sale_filter = self.env.ref('stock.view_picking_internal_search', False)
        action['search_view_id'] = sale_filter.id

        return action

    @api.multi
    def action_open_undone_receipt_orders(self):
        """return action based on type for related action"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'purchase':
                action_name = 'action_picking_tree_all'

        ctx = self._context.copy()
        ctx.update({
            'group_by': ['branch_id']

        })

        [action] = self.env.ref('stock.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', ['&', ('picking_type_id.code', '=', 'incoming'), '!',
                                                            ('state', 'in', ('done', 'cancel',))])
        sale_filter = self.env.ref('stock.view_picking_internal_search', False)
        action['search_view_id'] = sale_filter.id

        return action

    @api.multi
    def action_open_draft_stock_request(self):

        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'stock_request':
                action_name = 'action_requests'

        ctx = self._context.copy()
        """ctx.update({
            'group_by': [ 'date_order']

        })"""

        [action] = self.env.ref('nh_scm.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [ ('state', 'in', ('draft',)),

                                                            ])
        #stock_request_filter = self.env.ref('stock_request.view_stock_request_order_filter', False)
        #action['search_view_id'] = stock_request_filter.id

        return action

    @api.multi
    def action_open_approved_stock_request(self):
        requests, request_draft, request_approved, request_transit, request_done = \
            self._get_stock_requests_by_state()[0]
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'stock_request':
                action_name = 'action_requests'

        ctx = self._context.copy()
        """ctx.update({
            'group_by': [ 'date_order']

        })"""
        [action] = self.env.ref('nh_scm.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [('id', 'in', [r.id for r in request_approved]), ])
        # stock_request_filter = self.env.ref('stock_request.view_stock_request_order_filter', False)
        # action['search_view_id'] = stock_request_filter.id

        return action

    @api.multi
    def action_open_transit_stock_request(self):

        requests, request_draft, request_approved, request_transit, request_done = \
            self._get_stock_requests_by_state()[0]

        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'stock_request':
                action_name = 'action_requests'

        ctx = self._context.copy()
        """ctx.update({
            'group_by': [ 'date_order']

        })"""

        [action] = self.env.ref('nh_scm.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [('id', 'in', [r.id for r in request_transit]),

                                                            ])
        # stock_request_filter = self.env.ref('stock_request.view_stock_request_order_filter', False)
        # action['search_view_id'] = stock_request_filter.id

        return action

    @api.multi
    def action_open_done_stock_request(self):

        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'stock_request':
                action_name = 'action_requests'

        ctx = self._context.copy()
        """ctx.update({
            'group_by': [ 'date_order']

        })"""

        [action] = self.env.ref('nh_scm.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [ ('state', 'in', ('done',)),

                                                            ])
        #stock_request_filter = self.env.ref('stock_request.view_stock_request_order_filter', False)
        #action['search_view_id'] = stock_request_filter.id

        return action

    def _get_collect_amount(self, start_date, end_date):
        """if self.application != 'payment':
            return"""
        obj_acj = self.env['account.journal']
        journals = obj_acj.search([('type', 'in', ['cash', 'bank'])])
        total_debit = 0.0
        total_credit = 0.0

        for j in journals:
            for mv in self.env['account.move'].search(
                    [('journal_id', '=', j.id), ('date', '>=', start_date), ('date', '<=', end_date),
                     ('state', '=', 'posted')]):

                l1 = mv.line_ids[0]
                l2 = mv.line_ids[1]
                if l1.account_id.code.startswith(_cash_account_prefix) and l2.account_id.code.startswith(
                        _customer_account_prefix) or l1.account_id.code.startswith(
                    _bank_account_prefix) and l2.account_id.code.startswith(_customer_account_prefix):
                    if l2.credit != 0:
                        total_credit += l2.credit
                    elif l2.debit != 0:
                        total_debit += l2.debit

        collect_amount = total_credit - total_debit

        return collect_amount

    @api.one
    def _get_collect_total_week(self):
        """if self.application != 'payment':
            return"""
        dt = datetime.now()
        start_week = dt - timedelta(days=dt.weekday())
        end_week = start_week + timedelta(days=6)

        start_week_string = start_week.strftime('%Y-%m-%d') + ' 00:00:00'
        end_week_string = end_week.strftime('%Y-%m-%d') + ' 23:59:59'

        self.total_collect_weekly = self._get_collect_amount(start_week_string , end_week_string)

    @api.one
    def _get_collect_total_month(self):
        """if self.application != 'payment':
            return"""
        dt = datetime.now()
        start_string = dt.strftime('%Y-%m') + '-01 00:00:00'
        end_string = dt.strftime('%Y-%m-%d %H:%M:%S')

        self.total_collect_monthly = self._get_collect_amount(start_string, end_string)

    @api.one
    def _get_collect_total_year(self):
        """if self.application != 'payment':
            return"""
        dt = datetime.now()
        start_string = dt.strftime('%Y') + '-01-01 00:00:00'
        end_string = dt.strftime('%Y-%m-%d %H:%M:%S')

        self.total_collect_yearly = self._get_collect_amount(start_string, end_string)

    @api.multi
    def action_open_draft_invoice(self):

        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'payment':
                action_name = 'action_invoice_tree1'

        ctx = self._context.copy()
        """ctx.update({
            'group_by': [ 'date_order']

        })"""

        [action] = self.env.ref('account.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [('state', 'in', ('draft',)),])
        # stock_request_filter = self.env.ref('stock_request.view_stock_request_order_filter', False)
        # action['search_view_id'] = stock_request_filter.id

        return action

    @api.multi
    def action_open_open_invoice(self):
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application in( 'payment','customers'):
                action_name = 'action_invoice_tree1'

        ctx = self._context.copy()
        """ctx.update({
            'group_by': [ 'date_order']

        })"""

        [action] = self.env.ref('account.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [('state', 'in', ('open',)),

                                                            ])
        # stock_request_filter = self.env.ref('stock_request.view_stock_request_order_filter', False)
        # action['search_view_id'] = stock_request_filter.id

        return action

    @api.multi
    def action_open_paid_invoice(self):
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.application == 'payment':
                action_name = 'action_invoice_tree1'

        ctx = self._context.copy()
        """ctx.update({
            'group_by': [ 'date_order']

        })"""

        [action] = self.env.ref('account.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [('state', 'in', ('paid',)),

                                                            ])
        # stock_request_filter = self.env.ref('stock_request.view_stock_request_order_filter', False)
        # action['search_view_id'] = stock_request_filter.id

        return action
