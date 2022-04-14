from odoo import api, fields, models, _
import logging

class LandCostConfirmation(models.TransientModel):
    _name = 'nh_3n_pharma_land_cost.land_cost_confirmation_wizard'
    _description = 'Confirm Landing Cost'

    order_id = fields.Many2one('purchase.order', 'Purchase Order')

    transit_cost_mode = fields.Selection([
        ('cif', 'Cost Insurance and Freight (CIF)'),
        ('fob', 'Free on Board (FOB)'),
    ], string="Freight Mode")

    sgs_number = fields.Char("SGS Number")
    bill_of_landing_number = fields.Char("Bill of Landing Number")
    freight = fields.Float('Freight charges', help="freight forwarding charges from the supplier to the port")
    intervention_charge = fields.Float('Intervention Charge')
    outlay_charge = fields.Float('Outlay Charge')
    custom_cost = fields.Float('Custom Cost')
    handling_cost = fields.Float('Handling Cost')

    financial_expense_rate = fields.Float('Financial Expense rate in percentage')
    whithholding_on_sale_rate = fields.Float('Withholding on sale in percentage', default=1.0)
    external_audit_cost_rate = fields.Float('Import Audit Cost in percentage', default=0.95)

    financial_expense_value = fields.Float('Financial Expense', compute="_compute_all_charge")
    whithholding_on_sale_value = fields.Float('Withholding on sale', compute="_compute_all_charge")
    external_audit_cost_value = fields.Float('Import Audit Cost (SGS)', compute="_compute_all_charge")

    arrival_country = fields.Many2one('res.country', 'Arrival Country', default=lambda self: self._get_default_country())
    arrival_town = fields.Char('Arrival Town')
    currency_id = fields.Many2one('res.currency', "Currency", compute="_get_currency")

    land_cost_currency_id = fields.Many2one('res.currency',"Currency of the cost sheet")


    def _get_currency(self):
        for rec in self:
            rec.currency_id = rec.order_id.currency_id

    def _get_default_country(self):

        user_obj = self.env['res.users']

        user = user_obj.browse(self.env.user.id)

        return user.company_id.country_id

    def _compute_all_charge(self):

        for rec in self:
            rec.financial_expense_value = rec.currency_id.compute(rec.order_id.amount_total * rec.financial_expense_rate / 100,
                                                                  rec.land_cost_currency_id, False)
            rec.whithholding_on_sale_value = rec.currency_id.compute(
                rec.order_id.amount_total * rec.whithholding_on_sale_rate / 100, rec.land_cost_currency_id, False)
            rec.external_audit_cost_value = rec.currency_id.compute(
                rec.order_id.amount_total * rec.external_audit_cost_rate / 100, rec.land_cost_currency_id, False)


    @api.multi
    def action_confirm(self):
        vals = {
            'transit_cost_mode': self.transit_cost_mode,
            'freight':  self.freight,
            'intervention_charge':  self.intervention_charge,
            'outlay_charge':  self.outlay_charge,
            'custom_cost': self.custom_cost,
            'handling_cost': self.handling_cost,
            'financial_expense_rate': self.financial_expense_rate,
            'whithholding_on_sale_rate': self.whithholding_on_sale_rate,
            'external_audit_cost_rate': self.external_audit_cost_rate,
            'arrival_country': self.arrival_country.id,
            'arrival_town': self.arrival_town,
            'sgs_number' : self.sgs_number,
           
        }
        self.order_id.write(vals)

        land_cost_dict = {
            'order_id': self.order_id.id,
            'currency_id': self.land_cost_currency_id.id,
            'land_cost_line_ids': [],
        }

        for line in self.order_id.order_line:
            land_cost_dict['land_cost_line_ids'].append(
                (0, 0, {

                    'purchase_order_line_id': line.id,
                    'currency_id': self.land_cost_currency_id.id

                }
                 ))

        land_cost = self.env['nh_3n_pharma_land_cost.land_cost'].create(land_cost_dict)
        land_cost._read_order_data()

        for line in land_cost.land_cost_line_ids:
            line._read_line_data()

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'nh_3n_pharma_land_cost.land_cost',
            'target': 'current',
            'res_id': land_cost.id,
            'type': 'ir.actions.act_window'
        }

