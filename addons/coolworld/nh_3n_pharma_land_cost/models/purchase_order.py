# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
import logging
import datetime
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    _name = 'purchase.order'

    use_ratio_volume = fields.Boolean("Use ratio volume ?",
                                       help="It is to indicate if the products are not distributed"
                                            " separately in the containers. In the case where one"
                                            " can distinguish the volumes occupied by the products,"
                                            " this option must be selected.")



    land_cost_ids = fields.One2many('nh_3n_pharma_land_cost.land_cost', 'order_id', 'Landing Cost')
    has_land_cost = fields.Boolean(compute='_get_has_land_cost', string='Has Landing Cost ?')
    has_valid_land_cost = fields.Boolean(compute='_get_has_valid_land_cost', string='Has a draft or an approved landin cost ?')

    type = fields.Selection([('local', 'Local Purchase'), ('abroad', 'Import'), ('expense', 'Expense')], 'Type', default='local')
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('first_level_validation', 'Validation MD'),
        ('second_level_validation', 'Validation GM'),
        ('purchase', 'Purchase Order'),
        ('production', 'In Production'),
        ('transit', 'In Transit'),
        ('landed', 'Landed'),
        ('cost_saved', 'Landing Cost saved'),

        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')

    state_local = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('first_level_validation', 'Validation MD'),
        ('second_level_validation', 'Validation GM'),
        ('purchase', 'Purchase Order'),
        ('production', 'In Production'),
        ('transit', 'In Transit'),
        ('landed', 'Landed'),
        ('cost_saved', 'Landing Cost saved'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange', compute="_get_state")

    state_expense = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('first_level_validation', 'Validation MD'),
        ('second_level_validation', 'Validation GM'),
        ('purchase', 'Purchase Order'),
        ('production', 'In Production'),
        ('transit', 'In Transit'),
        ('landed', 'Landed'),
        ('cost_saved', 'Landing Cost saved'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange',
        compute="_get_state")


    #Variable for abroad purchase
    transit_cost_mode =  fields.Selection([
        ('cif', 'Cost Insurance and Freight (CIF)'),
        ('fob', 'Free on Board (FOB)'),
       ], string="Freight Mode")

    sgs_number = fields.Char("SGS Number")
    bill_of_landing_number = fields.Char("Bill of Landing Number")
    shipment_number = fields.Char("Shipment Number")

    minimun_percentage_before_approve = fields.Float('Minimun percentage to pay before approval')


    date_confirm = fields.Date('Confirmation Date')
    date_production_start = fields.Date('Went into production on')
    expected_production_end_date = fields.Date('Expected date of end of production')
    date_transit = fields.Date('Went into transit on')
    expected_landed_date = fields.Date('Expected Arrival Date (ETA)')
    date_arrival = fields.Date('Landed Date')
    date_cost_saved = fields.Date('Landing cost saved on')

    freight = fields.Float('Freight charges', help="freight forwarding charges from the supplier to the port")
    intervention_charge = fields.Float('Intervention Charge')
    outlay_charge = fields.Float('Outlay Charge')
    custom_cost = fields.Float('Custom Cost')
    handling_cost = fields.Float('Handling Cost')

    financial_expense_rate = fields.Float('Financial Expense rate in percentage', default = 20.0)
    whithholding_on_sale_rate = fields.Float('Withholding on sale in percentage', default = 1.0)
    external_audit_cost_rate = fields.Float('Import Audit Cost in percentage', default= 0.95)

    financial_expense_value = fields.Float('Financial Expense', compute="_compute_all_charge")
    whithholding_on_sale_value = fields.Float('Withholding on sale', compute="_compute_all_charge")
    external_audit_cost_value = fields.Float('Import Audit Cost (SGS)', compute="_compute_all_charge")

    origin_country = fields.Many2one('res.country', 'Country of purchase')
    arrival_country = fields.Many2one('res.country', 'Arrival Country' ,  default=lambda self: self._get_default_country())
    arrival_town = fields.Char('Arrival Town')

    amount_total_in_currency = fields.Float('Value of total amount in currency', compute="_compute_all_charge")
    land_costs_total = fields.Float('Total cost of landing', compute="_compute_all_charge")
    amount_total_with_land_costs = fields.Float('Total Purchase Price with Land Cost', compute="_compute_all_charge")

    
    
    #les valeurs recalculées après répartition par ratio
    freight_formula = fields.Float('Formula Freight charges', compute="_evaluate_difference")
    intervention_charge_formula = fields.Float('Formula Intervention Charge', compute="_evaluate_difference")
    outlay_charge_formula = fields.Float('Formula Outlay Charge', compute="_evaluate_difference")
    custom_cost_formula = fields.Float('Formula Custom Cost', compute="_evaluate_difference")
    handling_cost_formula = fields.Float('Formula Handling Cost', compute="_evaluate_difference")
    financial_expense_value_formula = fields.Float('Formula Financial Expense', compute="_evaluate_difference")
    whithholding_on_sale_value_formula = fields.Float('Formula Withholding on sale', compute="_evaluate_difference")
    external_audit_cost_value_formula = fields.Float('Formula Import Audit Cost (SGS)', compute="_evaluate_difference")
    land_costs_total_formula = fields.Float('Formula Total cost of landing', compute="_evaluate_difference")
    amount_total_formula = fields.Float('Formula Total Purchase Price',
                                                        compute="_evaluate_difference")
    amount_total_with_land_costs_formula = fields.Float('Formula Total Purchase Price with Land Cost',  compute="_evaluate_difference")

    # ecarts entre valeurs calculées et valeurs initiales
    freight_difference = fields.Float('Difference on Freight charges', compute="_evaluate_difference")
    intervention_charge_difference = fields.Float('Difference on Intervention Charge', compute="_evaluate_difference")
    outlay_charge_difference = fields.Float('Difference on Outlay Charge', compute="_evaluate_difference")
    custom_cost_difference = fields.Float('Difference on Custom Cost', compute="_evaluate_difference")
    handling_cost_difference = fields.Float('Difference on Handling Cost', compute="_evaluate_difference")
    financial_expense_value_difference = fields.Float('Difference on Financial Expense', compute="_evaluate_difference")
    whithholding_on_sale_value_difference = fields.Float('Difference on Withholding on sale', compute="_evaluate_difference")
    external_audit_cost_value_difference = fields.Float('Difference on Import Audit Cost (SGS)', compute="_evaluate_difference")
    land_costs_total_difference = fields.Float(' Difference on Total Purchase Price with Land Cost', compute="_evaluate_difference")
    amount_total_difference = fields.Float('Difference on Total Purchase',compute="_evaluate_difference")
    amount_total_with_land_costs_difference = fields.Float('Total Purchase Price with Land Cost',
                                                        compute="_evaluate_difference")

    land_cost_currency_id = fields.Many2one('res.currency','Currency of the cost sheet',default=lambda self: self._get_company_currency())



    #Variables for expenses purchases
    date_first_level_validation = fields.Date('MD validation date')
    date_second_level_validation = fields.Date('GM validation date')

    date_planned = fields.Datetime(string='Scheduled Date', compute='_compute_date_planned', store=True, index=True, default=fields.Datetime.now())



    def _get_default_country(self):
        user_obj = self.env['res.users']

        user = user_obj.browse(self.env.user.id)

        return user.company_id.country_id


    @api.model
    def _get_company_currency(self):
        return self.env.user.company_id.currency_id

    @api.constrains('minimun_percentage_before_approve', 'financial_expense_rate', 'whithholding_on_sale_rate',
                    'external_audit_cost_rate')
    def check_constraint(self):
        if (self.minimun_percentage_before_approve > 100.0 or self.minimun_percentage_before_approve < 0.0):
            raise UserError(_("The minimum percentage must be between 0 and 100"))
        if (self.financial_expense_rate > 100 or self.financial_expense_rate < 0):
            raise UserError(_("The Financial expenses rate must be between 0 and 100"))
        if (self.whithholding_on_sale_rate > 100 or self.whithholding_on_sale_rate < 0):
            raise UserError(_("The Sale Whithholding rate must be between 0 and 100"))
        if (self.external_audit_cost_rate > 100 or self.external_audit_cost_rate < 0):
            raise UserError(_("The External audit cost rate must be between 0 and 100"))

    def _compute_all_charge(self):
        for rec in self:
            rec.amount_total_in_currency = rec.currency_id.compute(rec.amount_total , rec.land_cost_currency_id,False)
            rec.land_costs_total = rec.freight + rec.intervention_charge +rec.outlay_charge + rec.custom_cost + rec.handling_cost
            rec.financial_expense_value = rec.currency_id.compute( rec.amount_total* rec.financial_expense_rate / 100 , rec.land_cost_currency_id,False)
            rec.whithholding_on_sale_value = rec.currency_id.compute( rec.amount_total * rec.whithholding_on_sale_rate / 100 , rec.land_cost_currency_id,False)
            rec.external_audit_cost_value = rec.currency_id.compute( rec.amount_total * rec.external_audit_cost_rate / 100 , rec.land_cost_currency_id,False)
            rec.land_costs_total +=  rec.financial_expense_value + rec.whithholding_on_sale_value + rec.external_audit_cost_value
            rec.amount_total_with_land_costs = rec.currency_id.compute(rec.amount_total , rec.land_cost_currency_id,False) + rec.land_costs_total




    def _evaluate_difference(self):

        for rec in self:
            rec.freight_formula = 0
            rec.intervention_charge_formula = 0
            rec.outlay_charge_formula = 0
            rec.custom_cost_formula = 0
            rec.handling_cost_formula = 0
            rec.financial_expense_value_formula = 0
            rec.whithholding_on_sale_value_formula = 0
            rec.external_audit_cost_value_formula = 0
            rec.land_costs_total_formula = 0
            rec.amount_total_formula = 0
            rec.amount_total_with_land_costs_formula = 0
            for line in rec.order_line:
                line._compute_all_charge()
                rec.freight_formula += line.line_freight
                rec.intervention_charge_formula += line.line_intervention_charge
                rec.outlay_charge_formula += line.line_outlay_charge
                rec.custom_cost_formula += line.line_custom_cost
                rec.handling_cost_formula += line.line_handling_cost
                rec.financial_expense_value_formula += line.line_financial_expense_value
                rec.whithholding_on_sale_value_formula += line.line_whithholding_on_sale_value
                rec.external_audit_cost_value_formula += line.line_external_audit_cost_value
                rec.amount_total_formula += rec.currency_id.compute(line.ratio*rec.amount_total/100 , rec.land_cost_currency_id)

                rec.amount_total_with_land_costs_formula +=  rec.currency_id.compute(line.price_total , rec.land_cost_currency_id,False)
            rec.land_costs_total_formula =  rec.freight_formula + rec.intervention_charge_formula +\
                                            rec.outlay_charge_formula + rec.custom_cost_formula + rec.handling_cost_formula +\
                                            rec.financial_expense_value_formula + rec.whithholding_on_sale_value_formula +\
                                            rec.external_audit_cost_value_formula
            rec.amount_total_with_land_costs_formula += rec.land_costs_total_formula

            rec.freight_difference = rec.freight_formula - rec.freight
            rec.intervention_charge_difference = rec.intervention_charge_formula - rec.intervention_charge
            rec.outlay_charge_difference = rec.outlay_charge_formula - rec.outlay_charge
            rec.custom_cost__difference = rec.custom_cost_formula - rec.custom_cost
            rec.handling_cost_difference = rec.handling_cost_formula - rec.handling_cost
            rec.financial_expense_value_difference = rec.financial_expense_value_formula- rec.financial_expense_value
            rec.whithholding_on_sale_value_difference = rec.whithholding_on_sale_value_formula -rec.whithholding_on_sale_value
            rec.external_audit_cost_value_difference = rec.external_audit_cost_value_formula -rec.external_audit_cost_value
            rec.land_costs_total_formula_difference = rec.land_costs_total_formula -rec.land_costs_total
            rec.amount_total_difference = rec.amount_total_formula - rec.amount_total_in_currency
            rec.amount_total_with_land_costs_difference = rec.amount_total_with_land_costs_formula -rec.amount_total_with_land_costs



    @api.multi
    def button_production(self):
        self.write({
            'state': 'production',
            'date_production_start' : fields.Datetime.now()
        })

    @api.multi
    def button_transit(self):
        self.write({
            'state': 'transit',
            'date_transit': fields.Datetime.now()
        })






    @api.multi
    def button_landed(self):
        self.write({
            'state': 'landed',
            'date_arrival': fields.Datetime.now()
        })

    @api.multi
    def button_generate_landing_cost(self):

        view = self.env.ref('nh_3n_pharma_land_cost.land_cost_confirmation_wizard')
        new_id = self.env['nh_3n_pharma_land_cost.land_cost_confirmation_wizard']

        vals = {
            'order_id' : self.id,
            'transit_cost_mode' : self.transit_cost_mode,
            'freight' : self.freight,
            'intervention_charge' : self.intervention_charge,
            'outlay_charge' : self.outlay_charge,
            'custom_cost' : self.custom_cost,
            'handling_cost' : self.handling_cost,
            'financial_expense_rate' : self.financial_expense_rate,
            'whithholding_on_sale_rate' : self.whithholding_on_sale_rate,
            'external_audit_cost_rate' : self.external_audit_cost_rate,
            'arrival_country' : self.arrival_country.id,
            'arrival_town'  :   self.arrival_town,
            'currency_id' : self.currency_id.id,
            'land_cost_currency_id' : self.land_cost_currency_id.id,
            'bill_of_landing_number' : self.bill_of_landing_number,
            'sgs_number' : self.sgs_number,

        }
        if (not self.arrival_country):
            user_obj = self.env['res.users']
            user = user_obj.browse(self.env.user.id)
            vals.update({'arrival_country' : user.company_id.country_id.id})

        view_id = new_id.create(vals)
        return {

            'type': 'ir.actions.act_window',

            'res_id': view_id.id,
            'view_type': 'form',

            'view_mode': 'form',

            'res_model': 'nh_3n_pharma_land_cost.land_cost_confirmation_wizard',

            'target': 'new',

        }


    @api.constrains('order_line' , 'use_ratio_volume','state')
    def check_volume_ratio(self):
        if self.use_ratio_volume and self.state in ['landed',]:
            precision = 0.001
            sum = 0
            for line in self.order_line:
                sum += line.volume_ratio

            if sum > 100+precision or sum < 100-precision:
                raise UserError( _("when you decided to use the volume ratio, the sum of the volume ratio must be 100"))






    @api.multi
    def button_cost_saved(self):
        self.write({
            'state': 'cost_saved',
            'date_cost_saved': fields.Datetime.now()
        })



    @api.multi
    def button_approve(self, force=False):
        if self.type == 'local':
            super(PurchaseOrder,self).button_approve()
        else:
            self.write({'state': 'purchase','date_confirm' : fields.Datetime.now()})




    @api.multi
    def button_draft(self):
        self.write({'state': 'draft'})
        return {}

    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent','second_level_validation']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step' \
                    or (order.company_id.po_double_validation == 'two_step' \
                        and order.amount_total < self.env.user.company_id.currency_id.compute(
                        order.company_id.po_double_validation_amount, order.currency_id)) \
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        return True

    @api.multi
    def button_confirm_local(self):
        return  super(PurchaseOrder,self).button_confirm()

    @api.multi
    def action_view_land_cost(self):
        '''
        This function returns an action that display existing land cost
        of given purchase ids. It can either be a in a list or in a form
        view, if there is only one stock picking to show.
        '''
        action = self.env.ref('nh_3n_pharma_land_cost.action_landing_cost').read()[0]

        land_costs = self.mapped('land_cost_ids')
        if len(land_costs) > 1:
            action['domain'] = [('id', 'in', land_costs.ids)]
        elif land_costs:
            action['views'] = [(self.env.ref('nh_3n_pharma_land_cost.landing_cost_form').id, 'form')]
            action['res_id'] = land_costs.id
        return action

    def _get_has_land_cost(self):

        for rec in self:
            if (rec.land_cost_ids):
                rec.has_land_cost = True
            else:
                rec.has_land_cost = False

    def _get_has_valid_land_cost(self):

        for rec in self:
            lands =self.env['nh_3n_pharma_land_cost.land_cost'].search(['&',('order_id','=',self.id),('state','in',('draft','approved'))])
            if lands :
                rec.has_valid_land_cost = True
            else:
                rec.has_valid_land_cost = False


    def _get_state(self):
        for rec in self:
            rec.state_local = rec.state
            rec.state_expense = rec.state





    #expense workflow button actions

    @api.multi
    def button_first_level_validation(self):
        self.write({
            'state': 'first_level_validation',
            'date_first_level_validation': fields.Datetime.now()
        })


    @api.multi
    def button_second_level_validation(self):
        self.write({
            'state': 'second_level_validation',
            'date_second_level_validation': fields.Datetime.now()
        })
        return self.button_confirm()

    @api.multi
    @api.constrains('type')
    def check_type(self):
        for line in  self.order_line:
            if self.type == 'expense' and not line.product_id.product_tmpl_id.control_expense:
                raise UserError(_(
                    'For Expense, you have to choose only product on whitch control expense is activated'))
            if self.type != 'expense' and line.product_id.product_tmpl_id.control_expense:
                raise UserError(_(
                    'For Purchase of not Expense type, you can\'t choose  product on whitch control expense is activated'))
        return  True