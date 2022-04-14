# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import UserError


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    _name = 'purchase.order.line'

    use_ratio_volume = fields.Boolean("Use ratio volume ?",
                                       help="It is to indicate if the products are not distributed"
                                            " separately in the containers. In the case where one"
                                            " can distinguish the volumes occupied by the products,"
                                            " this option must be selected.", compute = "_get_use_volume_ratio")
    ratio = fields.Float(compute='_get_ratio', string="ratio per quantity", help='Ratio of the line price on the purchase Total price')
    volume_ratio = fields.Float(string="Volume ratio in %", help='The volume ratio indicates the volume proportion of the article on'
                                                     ' the total carcase (the volume can be estimated as the number '
                                                     'of containers occupied)')

    line_freight = fields.Float('Freight charges', help="freight forwarding charges from the supplier to the port",comute="_compute_all_charge")
    line_intervention_charge = fields.Float('Intervention Charge', compute="_compute_all_charge")
    line_outlay_charge = fields.Float('Outlay Charge' , compute = "_compute_all_charge")
    line_custom_cost = fields.Float('Custom Cost', compute = "_compute_all_charge")
    line_handling_cost = fields.Float('Handling Cost', compute = "_compute_all_charge")
    line_financial_expense_value = fields.Float('Financial Expense' , compute = "_compute_all_charge")
    line_whithholding_on_sale_value = fields.Float('Withholding on sale' , compute="_compute_all_charge" )
    line_external_audit_cost_value = fields.Float('Import Audit Cost' , compute = "_compute_all_charge")

    global_cost_purchase = fields.Float('Global Cost Price', compute="_compute_global_cost_purchase")
    cost_per_unit_purchase = fields.Float('Cost  Per unit purchase', compute="_compute_global_cost_purchase")
    stock_available_qty = fields.Float(compute='_get_all_qty_in_stock', string='Quantity of the product in stock')

    final_average_cost_price = fields.Float(compute="_get_final_average_price", string=" Final  Cost Price")
    date_planned = fields.Datetime(string='Scheduled Date', default=fields.Datetime.now(),required=False, index=True)

    type = fields.Char(compute="_get_type")

    def _get_type(self):
        for rec in self:
            rec.type = rec.order_id.type



    @api.constrains('volume_ratio')
    def check_volume_ratio(self):
        if self.volume_ratio > 100 or self.volume_ratio < 0:
            raise UserError(_("Volume ratio must be between 0 and 100"))

    def _get_ratio(self):
        for rec in self:
            if rec.order_id.amount_total != 0 :
                rec.ratio = rec.price_total*100/rec.order_id.amount_total

    def _get_use_volume_ratio(self):
        for rec in self:
            rec.use_ratio_volume = rec.order_id.use_ratio_volume



    def _compute_all_charge(self):

        for rec in self :

            rec.line_intervention_charge = rec.ratio * rec.order_id.intervention_charge / 100

            rec.line_custom_cost = rec.ratio * rec.order_id.custom_cost / 100

            rec.line_financial_expense_value = rec.ratio * rec.order_id.financial_expense_value / 100
            rec.line_whithholding_on_sale_value = rec.ratio * rec.order_id.whithholding_on_sale_value / 100
            rec.line_external_audit_cost_value = rec.ratio * rec.order_id.external_audit_cost_value / 100
            if rec.use_ratio_volume:
                rec.line_handling_cost = rec.volume_ratio * rec.order_id.handling_cost / 100
                rec.line_outlay_charge = rec.volume_ratio * rec.order_id.outlay_charge / 100
                rec.line_freight = rec.volume_ratio * rec.order_id.freight / 100

            else:
                rec.line_handling_cost = rec.ratio * rec.order_id.handling_cost / 100
                rec.line_outlay_charge = rec.ratio * rec.order_id.outlay_charge / 100
                rec.line_freight = rec.ratio * rec.order_id.freight / 100






    def _compute_global_cost_purchase(self):
        for rec in self :
            rec.global_cost_purchase = rec.currency_id.compute(rec.price_total , rec.order_id.land_cost_currency_id,False) + rec.line_freight + rec.line_intervention_charge\
                                       + rec.line_outlay_charge + rec.line_custom_cost + rec.line_handling_cost \
                                       + rec.line_financial_expense_value + rec.line_whithholding_on_sale_value \
                                       + rec.line_external_audit_cost_value
            rec.cost_per_unit_purchase = rec.global_cost_purchase
            if (rec.product_qty !=0):
                rec.cost_per_unit_purchase/=rec.product_qty



    def _get_all_qty_in_stock(self):
        for rec in self:
            rec.stock_available_qty  = rec.product_id.qty_available
            rec.stock_available_qty = rec.product_uom._compute_quantity(rec.stock_available_qty, rec.product_id.uom_id, rounding_method='HALF-UP')


    def _get_final_average_price(self):
        for rec in self :
            den = rec.stock_available_qty + rec.product_qty
            #le cout global contient la qté commandée
            if (den!=0):
                num = rec.global_cost_purchase + rec.product_id.standard_price * rec.stock_available_qty
                rec.final_average_cost_price = num/den


    @api.constrains('product_id')
    def check_type(self):

        if self.order_id.type == 'expense' and not  self.product_id.product_tmpl_id.control_expense:
            raise UserError(_(
                'For Expense, you have to choose only product on whitch control expense is activated'))
        if self.order_id.type != 'expense' and  self.product_id.product_tmpl_id.control_expense:
            raise UserError(_(
                'For Purchase of not Expense type, you can\'t choose  product on whitch control expense is activated'))

    @api.depends('order_id.state', 'move_ids.state', 'move_ids.product_uom_qty')
    def _compute_qty_received(self):
        for line in self:
            if line.order_id.state not in ['purchase','cost_saved','done']:
                line.qty_received = 0.0
                continue
            if line.product_id.type not in ['consu', 'product']:
                line.qty_received = line.product_qty
                continue
            total = 0.0
            for move in line.move_ids:
                if move.state == 'done':
                    if move.location_dest_id.usage == "supplier":
                        if move.to_refund:
                            total -= move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
                    else:
                        total += move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
            line.qty_received = total


