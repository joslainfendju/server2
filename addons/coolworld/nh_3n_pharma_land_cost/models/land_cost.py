# -*- coding: utf-8 -*-


from odoo import api, fields, models,_
import  logging


_logger = logging.getLogger(__name__)



class LandCost(models.Model):
    _name = 'nh_3n_pharma_land_cost.land_cost'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    order_id = fields.Many2one("purchase.order", 'Purchase Order')
    currency_id = fields.Many2one('res.currency', "Currency")
    name = fields.Char('Name')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')

    transit_cost_mode = fields.Selection([
        ('cif', 'Cost Insurance and Freight (CIF)'),
        ('fob', 'Free on Board (FOB)'),
    ], string="Freight Mode", compute="_read_order_data",store=True)

    use_ratio_volume = fields.Boolean("Use ratio volume ?",
                                      help="It is to indicate if the products are not distributed"
                                           " separately in the containers. In the case where one"
                                           " can distinguish the volumes occupied by the products,"
                                           " this option must be selected." , compute="_read_order_data",store=True)

    date_approve = fields.Date('Approve Date')
    date_cancel = fields.Date('Date cancel')
    date_done = fields.Date('Date done')

    freight = fields.Float('Freight charges', help="freight forwarding charges from the supplier to the port" , compute="_read_order_data",store=True)
    intervention_charge = fields.Float('Intervention Charge' , compute="_read_order_data",store=True)
    outlay_charge = fields.Float('Outlay Charge' , compute="_read_order_data" , store=True)
    custom_cost = fields.Float('Custom Cost' , compute="_read_order_data" , store=True)
    handling_cost = fields.Float('Handling Cost' , compute="_read_order_data" , store=True)

    financial_expense_rate = fields.Float('Financial Expense rate in percentage', default=20.0 , compute="_read_order_data" , store=True)
    whithholding_on_sale_rate = fields.Float('Withholding on sale in percentage', default=1.0, compute="_read_order_data" , store=True)
    external_audit_cost_rate = fields.Float('Import Audit Cost in percentage', default=0.95, compute="_read_order_data" , store=True)

    financial_expense_value = fields.Float('Financial Expense',  compute="_read_order_data" , store=True)
    whithholding_on_sale_value = fields.Float('Withholding on sale', compute="_read_order_data" , store=True)
    external_audit_cost_value = fields.Float('Import Audit Cost (SGS)',  compute="_read_order_data" , store=True)

    land_cost_line_ids = fields.One2many('nh_3n_pharma_land_cost.land_cost_line', 'land_cost_id', 'Land Cost Line')

    amount_total =  fields.Float('Total Purchase Price',  compute="_read_order_data" , store=True)
    land_costs_total = fields.Float('Total cost of landing', compute="_read_order_data",store=True)
    amount_total_with_land_costs = fields.Float('Total Purchase Price with Land Cost', compute="_read_order_data", store=True)

    # les valeurs recalculées après répartition par ratio
    freight_formula = fields.Float('Formula Freight charges', compute="_read_order_data", store=True)
    intervention_charge_formula = fields.Float('Formula Intervention Charge', compute="_read_order_data", store=True)
    outlay_charge_formula = fields.Float('Formula Outlay Charge', compute="_read_order_data", store=True)
    custom_cost_formula = fields.Float('Formula Custom Cost', compute="_read_order_data", store=True)
    handling_cost_formula = fields.Float('Formula Handling Cost', compute="_read_order_data", store=True)
    financial_expense_value_formula = fields.Float('Formula Financial Expense', compute="_read_order_data", store=True)
    whithholding_on_sale_value_formula = fields.Float('Formula Withholding on sale', compute="_read_order_data", store=True)
    external_audit_cost_value_formula = fields.Float('Formula Import Audit Cost (SGS)', compute="_read_order_data", store=True)
    land_costs_total_formula = fields.Float('Formula Total cost of landing',
                                            compute="_read_order_data", store=True)
    amount_total_formula = fields.Float('Formula Total Purchase Price',
                                        compute="_read_order_data" , store=True)
    amount_total_with_land_costs_formula = fields.Float('Formula Total Purchase Price with Land Cost',
                                                        compute="_read_order_data", store=True)

    # ecarts entre valeurs calculées et valeurs initiales
    freight_difference = fields.Float('Difference on Freight charges', compute="_read_order_data", store=True)
    intervention_charge_difference = fields.Float('Difference on Intervention Charge', compute="_read_order_data", store=True)
    outlay_charge_difference = fields.Float('Difference on Outlay Charge', compute="_read_order_data", store=True)
    custom_cost_difference = fields.Float('Difference on Custom Cost', compute="_read_order_data", store=True)
    handling_cost_difference = fields.Float('Difference on Handling Cost', compute="_read_order_data", store=True)
    financial_expense_value_difference = fields.Float('Difference on Financial Expense', compute="_read_order_data", store=True)
    whithholding_on_sale_value_difference = fields.Float('Difference on Withholding on sale',
                                                      compute="_read_order_data", store=True)
    external_audit_cost_value_difference = fields.Float('Difference on Import Audit Cost (SGS)',
                                                     compute="_read_order_data", store=True)
    land_costs_total_difference = fields.Float('Difference on Total Purchase Price with Landing Costs',
                                            compute="_read_order_data", store=True)
    amount_total_difference = fields.Float('Difference on Total Purchase',  compute="_read_order_data", store=True)
    amount_total_with_land_costs_difference = fields.Float('Difference on Total Purchase Price with Landing Costs',
                                                        compute="_read_order_data", store=True)



    def _read_order_data(self):
        for rec in self:
            rec.transit_cost_mode = rec.order_id.transit_cost_mode

            rec.freight =rec.order_id.freight
            rec.intervention_charge =rec.order_id.intervention_charge
            rec.outlay_charge  =rec.order_id.outlay_charge 
            rec.custom_cost =rec.order_id.custom_cost
            rec.handling_cost =rec.order_id.handling_cost
            rec.financial_expense_rate =rec.order_id.financial_expense_rate
            rec.whithholding_on_sale_rate =rec.order_id. whithholding_on_sale_rate
            rec.external_audit_cost_rate =rec.order_id.external_audit_cost_rate
            rec.financial_expense_value =rec.order_id.financial_expense_value
            rec.whithholding_on_sale_value =rec.order_id.whithholding_on_sale_value
            rec.external_audit_cost_value =rec.order_id.external_audit_cost_value

            rec.amount_total =rec.order_id.currency_id.compute(rec.order_id.amount_total , rec.currency_id,False)
            rec.land_costs_total = rec.order_id.land_costs_total
            rec.amount_total_with_land_costs = rec.order_id.amount_total_with_land_costs

            rec.freight_formula = rec.order_id.freight_formula
            rec.intervention_charge_formula = rec.order_id.intervention_charge_formula
            rec.outlay_charge_formula = rec.order_id.outlay_charge_formula
            rec.custom_cost_formula = rec.order_id.custom_cost_formula
            rec.handling_cost_formula = rec.order_id.handling_cost_formula
            rec.financial_expense_value_formula = rec.order_id.financial_expense_value_formula
            rec.whithholding_on_sale_value_formula = rec.order_id.whithholding_on_sale_value_formula
            rec.external_audit_cost_value_formula = rec.order_id.external_audit_cost_value_formula
            rec.land_costs_total_formula = rec.order_id.land_costs_total_formula
            rec.amount_total_formula = rec.order_id.amount_total_formula
            rec.amount_total_with_land_costs_formula = rec.order_id.amount_total_with_land_costs_formula

            rec.freight_difference = rec.order_id.freight_difference
            rec.intervention_charge_difference = rec.order_id.intervention_charge_difference
            rec.outlay_charge_difference = rec.order_id.outlay_charge_difference
            rec.custom_cost_difference = rec.order_id.custom_cost_difference
            rec.handling_cost_difference = rec.order_id.handling_cost_difference
            rec.financial_expense_value_difference = rec.order_id.financial_expense_value_difference
            rec.whithholding_on_sale_value_difference = rec.order_id.whithholding_on_sale_value_difference
            rec.external_audit_cost_value_difference = rec.order_id.external_audit_cost_value_difference
            rec.land_costs_total_difference = rec.order_id.land_costs_total_difference
            rec.amount_total_difference = rec.order_id.amount_total_difference
            rec.amount_total_with_land_costs_difference = rec.order_id.amount_total_with_land_costs_difference

            rec.use_ratio_volume = rec.order_id.use_ratio_volume

            rec.write(
                {
                    'transit_cost_mode' : rec.transit_cost_mode,

                    'freight' :  rec.freight,
                    'intervention_charge' :   rec.intervention_charge,
                    'outlay_charge' :  rec.outlay_charge,
                    'custom_cost' :   rec.custom_cost,
                    'handling_cost' :   rec.handling_cost,
                    'financial_expense_rate' : rec.financial_expense_rate,
                    'whithholding_on_sale_rate' : rec.whithholding_on_sale_rate,
                    'external_audit_cost_rate' : rec.external_audit_cost_rate,
                    'financial_expense_value' :   rec.financial_expense_value,
                    'whithholding_on_sale_value' :   rec.whithholding_on_sale_value,
                    'external_audit_cost_value' :   rec.external_audit_cost_value,
                    'amount_total' :   rec.amount_total,
                    'land_costs_total' :   rec.land_costs_total,
                    'amount_total_with_land_costs' :  rec.amount_total_with_land_costs,
                    'freight_formula' :   rec.freight_formula,
                    'intervention_charge_formula' :   rec.intervention_charge_formula,
                    'outlay_charge_formula' :   rec.outlay_charge_formula,
                    'custom_cost_formula' :   rec.custom_cost_formula,
                    'handling_cost_formula' :  rec.handling_cost_formula,
                    'financial_expense_value_formula' :   rec.financial_expense_value_formula,
                    'whithholding_on_sale_value_formula' :  rec.whithholding_on_sale_value_formula,
                    'external_audit_cost_value_formula' :   rec.external_audit_cost_value_formula,
                    'land_costs_total_formula' :   rec.land_costs_total_formula,
                    'amount_total_formula':  rec.amount_total_formula ,
                    'amount_total_with_land_costs_formula' :  rec.amount_total_with_land_costs_formula,
                    'freight_difference' :   rec.freight_difference ,
                    'intervention_charge_difference' :   rec.intervention_charge_difference,
                    'outlay_charge_difference' :   rec.outlay_charge_difference,
                    'custom_cost_difference' :   rec.custom_cost_difference,
                    'handling_cost_difference' :   rec.handling_cost_difference,
                    'financial_expense_value_difference' :   rec.financial_expense_value_difference,
                    'whithholding_on_sale_value_difference' :  rec.whithholding_on_sale_value_difference,
                    'external_audit_cost_value_difference' :   rec.external_audit_cost_value_difference,
                    'land_costs_total_difference' :   rec.land_costs_total_difference,
                    'amount_total_difference' :   rec.amount_total_difference,
                    'amount_total_with_land_costs_difference' :  rec.amount_total_with_land_costs_difference,

                    'use_ratio_volume': rec.use_ratio_volume,

                }
            )



    @api.multi
    def button_approve(self):
        self.write({
            'state': 'approved',
            'date_approve': fields.Datetime.now()
        })
        self.order_id.write({
            'state': 'cost_saved',
            'date_cost_saved': fields.Datetime.now()
        })
        logging.info('save approved*************')
        for line in self.land_cost_line_ids:
            old_cost_price = line.purchase_order_line_id.product_id.standard_price
            line.product_id.write(
                {
                    #'standard_price': line.cost_price_after_purchase ,
                    'standard_price': line.cost_per_unit_purchase,
                }
            )
            self.env['nh_3n_pharma_land_cost.land_cost_log'].create(
                {
                    'land_cost_id': self.id,
                    'land_cost_line_id': line.id,
                    'product_template_id': line.product_id.product_tmpl_id.id,
                    'old_product_qty': line.stock_before_arrival,
                    'old_product_cost': old_cost_price,
                    'landed_product_qty': line.purchase_qty,
                    'landed_product_cost': line.global_cost_purchase,
                    #'new_product_cost': line.product_id.standard_price,
                    'new_product_cost': line.product_id.standard_price,
                    'date_log': fields.Datetime.now(),
                }
            )
        logging.info('save logged *************')
        self.order_id._create_picking()
        logging.info('create picking*************')
        self.order_id.button_cost_saved()
        logging.info('cost saved*************')
        if self.order_id.company_id.po_lock == 'lock':
            self.order_id.write({'state': 'done'})

        logging.info('finish*************')

        return {}

    @api.multi
    def button_cancel(self):
        self.write({
            'state': 'cancel',
            'date_cancel': fields.Datetime.now()
        })

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'nh_3n_pharma_land_cost.seq_nh_3n_pharma_land_cost_land_cost') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('nh_3n_pharma_land_cost.land_cost') or _('New')

        result = super(LandCost, self).create(vals)
        return result



    @api.multi
    def button_print(self):
        #view = self.env.ref('nh_3n_pharma_land_cost.land_cost_export_wizard')
        new_id = self.env['nh_3n_pharma_land_cost.land_cost_export_wizard']

        vals = {
            'land_cost_id': self.id,

        }

        view_id = new_id.create(vals)
        return {

            'type': 'ir.actions.act_window',

            'res_id': view_id.id,
            'view_type': 'form',

            'view_mode': 'form',

            'res_model': 'nh_3n_pharma_land_cost.land_cost_export_wizard',

            'target': 'new',

        }