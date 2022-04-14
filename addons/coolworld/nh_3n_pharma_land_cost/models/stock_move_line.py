# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from odoo import models, fields, api


class  StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    _name = 'stock.move.line'

    landing_cost = fields.Float('Landing Cost')
    land_cost_line_id = fields.Many2one("nh_3n_pharma_land_cost.land_cost_line", 'Cost Details')
    
    @api.model
    def create(self, vals):
        res = super(StockMoveLine, self).create(vals)

        if res.move_id.picking_id and res.move_id.picking_id.purchase_id and res.move_id.picking_id.purchase_id.type == 'abroad':
            purchase = res.move_id.picking_id.purchase_id
            land_cost_line_approved = self.env['nh_3n_pharma_land_cost.land_cost_line'].search(['&',('land_cost_id.order_id','=',purchase.id),'&',('land_cost_id.state', '=', 'approved'),('product_id','=',res.product_id.id)])
            lcl = land_cost_line_approved[0]
            res.write(
                {
                    'landing_cost' : lcl.cost_price_after_purchase,
                    'land_cost_line_id': lcl.id

                }
            )

        return res


