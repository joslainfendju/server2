# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from openerp.exceptions import ValidationError
from odoo.tools import config, float_compare
import datetime
import logging



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # @api.multi
    # def action_done(self):
    #
    #     self.checkLoc_LotAvailableQuant()
    #
    #     return  super(StockPicking, self).action_done()


    def checkLoc_LotAvailableQuant(self):

        reference=self.picking_type_code

        if reference in ['outgoing','internal'] :

            location_id = self.location_id.id
            move_lines = self.move_line_ids
            available_qty=0
            product_qty=0

            for mvl in move_lines:
                moves_lots = mvl.lot_id

                if len(moves_lots) == 1:

                    available_qty = mvl.product_id.with_context(
                        {'location': location_id, 'lot_id': moves_lots.id}).qty_available

                    if available_qty <0:
                        raise ValidationError(_('Le numero de lot :' + str(
                            moves_lots.name) + '\tne contient pas assez de produits pour faire cette operation' + '\nBien vouloir verifier votre stock et choisir un autre lot au besoin\n Quantité en moins:\t' + str(
                            abs(available_qty- mvl.qty_done))))
                elif len(moves_lots) > 1:
                    for lot in moves_lots:
                        available_qty = mvl.product_id.with_context(
                            {'location': location_id, 'lot_id': lot.id}).qty_available

                        if (available_qty < 0):
                            raise ValidationError(_('Le numero de lot :' + str(
                                lot.name) + '\tne contient pas assez de produits pour faire cette operation' + '\nBien vouloir verifier votre stock et choisir un autre lot au besoin\n Quantité en moins:\t' + str(
                                abs(available_qty-mvl.qty_done))))

    # @api.multi
    # def button_validate(self):
    #
    #     res = super(StockPicking, self).button_validate()
    #     self.checkLoc_LotAvailableQuant()
    #     return  res
    #
    # @api.multi
    # def write(self, vals):
    #
    #     if 'state' in vals and vals['state'] == 'done':
    #         self.checkLoc_LotAvailableQuant()
    #
    #     return  super(StockPicking, self).write(vals)

# class stock_immediat_transfer(models.TransientModel):
#     _name = 'stock.immediate.transfer'
#     _inherit = 'stock.immediate.transfer'
#
#
#     def process(self):
#         res=super(stock_immediat_transfer,self).process()
#         for picking in self.pick_ids:
#             picking.checkLoc_LotAvailableQuant()
#         return res
#
#
# class StockBackorderConfirmation(models.TransientModel):
#     _inherit = 'stock.backorder.confirmation'
#     _description = 'Backorder Confirmation'
#
#     def process(self):
#         res=super(StockBackorderConfirmation, self).process()
#         for picking in self.pick_ids:
#             picking.checkLoc_LotAvailableQuant()
#
#         return res

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.multi
    @api.constrains('product_id', 'quantity')
    def check_negative_qty(self):
        p = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')

        for quant in self:

            if (
                float_compare(quant.quantity, 0, precision_digits=p) == -1 and
                quant.product_id.type == 'product' and
                quant.location_id.usage in ['internal', 'transit']

            ):
                msg_add = ''
                if quant.lot_id:
                    untracked_qty = quant._get_available_quantity(
                        quant.product_id, quant.location_id, lot_id=quant.lot_id,
                        strict=True)
                    if float_compare(abs(quant.quantity),
                                     untracked_qty, precision_digits=p) < 1:
                        return True
                    msg_add = _("lot '%s'") % quant.lot_id.display_name

                else:
                    untracked_qty = quant._get_available_quantity(
                        quant.product_id, quant.location_id, lot_id=False,
                        strict=True)
                    if float_compare(abs(quant.quantity),
                                     untracked_qty, precision_digits=p) < 1:
                        return True
                    msg_add =" "
                raise ValidationError(_(
                    "You cannot validate this stock operation because\n the "
                    "stock level of the product '%s'%s would become negative "
                    "(%s) on the stock location '%s' and\n negative stock is "
                    "not allowed.") % (
                        quant.product_id.name, msg_add, quant.quantity,
                        quant.location_id.complete_name))
