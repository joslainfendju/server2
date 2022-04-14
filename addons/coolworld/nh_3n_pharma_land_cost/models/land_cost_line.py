#-*- coding: utf-8 -*-

from odoo import models, fields, api,_
import logging
import datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)



class LandCostLine(models.Model):
    _name = 'nh_3n_pharma_land_cost.land_cost_line'

    land_cost_id = fields.Many2one("nh_3n_pharma_land_cost.land_cost", 'Parent')
    purchase_order_line_id = fields.Many2one("purchase.order.line", 'Order Line')
    product_id = fields.Many2one("product.product", 'Product', compute="_read_line_data", store=True)
    use_ratio_volume = fields.Boolean("Use ratio volume ?",
                                      help="It is to indicate if the products are not distributed"
                                           " separately in the containers. In the case where one"
                                           " can distinguish the volumes occupied by the products,"
                                           " this option must be selected.", compute="_read_line_data", store=True)

    ratio = fields.Float(string='Ratio', help ="Ratio of the line price on the purchase Total price", compute="_read_line_data", store=True)
    volume_ratio = fields.Float(string="Volume ratio in %",
                                help='The volume ratio indicates the volume proportion of the article on'
                                     ' the total carcase (the volume can be estimated as the number '
                                     'of containers occupied)', compute="_read_line_data", store=True)

    line_freight = fields.Float('Freight charges', help="freight forwarding charges from the supplier to the port",
                                compute="_read_line_data", store=True)
    purchase_unit_price = fields.Float("Purchase Unit Price")
    purchase_qty = fields.Float("Purchase quantity",  compute="_read_line_data"  , store=True)
    purchase_price = fields.Float("Purchase Price",  compute="_read_line_data"  , store=True)

    line_intervention_charge = fields.Float('Intervention Charge', compute="_read_line_data"  , store=True)
    line_outlay_charge = fields.Float('Outlay Charge', compute="_read_line_data"  , store=True)
    line_custom_cost = fields.Float('Custom Cost', compute="_read_line_data"  , store=True)
    line_handling_cost = fields.Float('Handling Cost', compute="_read_line_data"  , store=True)
    line_financial_expense_value = fields.Float('Financial Expense', compute="_read_line_data"  , store=True)
    line_whithholding_on_sale_value = fields.Float('Withholding on sale', compute="_read_line_data"  , store=True)
    line_external_audit_cost_value = fields.Float('Import Audit Cost', compute="_read_line_data"  , store=True)

    global_cost_purchase = fields.Float('Global Cost Price', compute="_read_line_data" , store=True)
    cost_per_unit_purchase = fields.Float('Cost  Per unit purchase', compute="_read_line_data" , store=True)

    stock_before_arrival = fields.Float('Stock before arrival')
    cost_before_purchase = fields.Float('Cost before arrival')

    cost_price_after_purchase = fields.Float('Final Cost Price',  compute="_read_line_data" , store=True)

    currency_id = fields.Many2one('res.currency',"Currency")



    def _read_line_data(self):
        for rec in self:

            rec.product_id = rec.purchase_order_line_id.product_id

            rec.ratio = rec.purchase_order_line_id.ratio
            rec.line_freight = rec.purchase_order_line_id.line_freight
            rec.purchase_unit_price = rec.purchase_order_line_id.currency_id.compute(rec.purchase_order_line_id.price_unit , rec.currency_id,False)
            rec.purchase_qty = rec.purchase_order_line_id.product_qty
            rec.line_intervention_charge = rec.purchase_order_line_id.line_intervention_charge
            rec.line_outlay_charge = rec.purchase_order_line_id.line_outlay_charge
            rec.line_custom_cost  = rec.purchase_order_line_id.line_custom_cost
            rec.line_handling_cost = rec.purchase_order_line_id.line_handling_cost
            rec.line_financial_expense_value = rec.purchase_order_line_id.line_financial_expense_value
            rec.line_whithholding_on_sale_value = rec.purchase_order_line_id.line_whithholding_on_sale_value
            rec.line_external_audit_cost_value  = rec.purchase_order_line_id.line_external_audit_cost_value
            rec.global_cost_purchase = rec.purchase_order_line_id.global_cost_purchase
            rec.cost_per_unit_purchase  = rec.purchase_order_line_id.cost_per_unit_purchase
            rec.stock_before_arrival = rec.purchase_order_line_id.stock_available_qty
            rec.cost_before_purchase  = rec.purchase_order_line_id.product_id.standard_price
            rec.cost_price_after_purchase = rec.purchase_order_line_id.final_average_cost_price

            rec.purchase_price = rec.purchase_order_line_id.currency_id.compute(rec.purchase_order_line_id.price_total , rec.currency_id,False)
            rec.use_ratio_volume = rec.purchase_order_line_id.use_ratio_volume
            rec.volume_ratio = rec.purchase_order_line_id.volume_ratio


            rec.write(
                {
                    'product_id' : rec.purchase_order_line_id.product_id.id,

                    'ratio'  : rec.purchase_order_line_id.ratio,

                    'line_freight' :  rec.line_freight,
                    'purchase_unit_price' : rec.purchase_unit_price,

                    'purchase_qty' : rec.purchase_qty,

                    'line_intervention_charge' : rec.line_intervention_charge ,
                    'line_outlay_charge' :  rec.line_outlay_charge,
                    'line_custom_cost' :  rec.line_custom_cost ,
                    'line_handling_cost' :  rec.line_handling_cost,
                    'line_financial_expense_value' :  rec.line_financial_expense_value,
                    'line_whithholding_on_sale_value' :  rec.line_whithholding_on_sale_value ,
                    'line_external_audit_cost_value' :  rec.line_external_audit_cost_value,
                    'global_cost_purchase' :  rec.global_cost_purchase ,
                    'cost_per_unit_purchase' : rec.cost_per_unit_purchase,

                    'stock_before_arrival' : rec.stock_before_arrival,

                    'cost_before_purchase' :  rec.cost_before_purchase,
                    'cost_price_after_purchase' :  rec.cost_price_after_purchase ,

                    'purchase_price' :  rec.purchase_price,

                    'use_ratio_volume' : rec.use_ratio_volume,
                    'volume_ratio' : rec.volume_ratio

                }
            )



