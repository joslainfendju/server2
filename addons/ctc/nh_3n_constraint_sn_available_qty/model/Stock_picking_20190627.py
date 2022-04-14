# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from openerp.exceptions import ValidationError

import datetime
import logging



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # def checkSpoil(self):
    #
    #     move_lines = self.move_lines
    #     today_date=datetime.datetime.now().date()
    #     for mvl in move_lines:
    #         moves_lots=mvl.lot_ids
    #
    #         if len(moves_lots)==1:
    #             life_date_obj = datetime.datetime.strptime(moves_lots.life_date, '%Y-%m-%d %H:%M:%S')
    #             life_date=life_date_obj.date()
    #             if(today_date<life_date):
    #                 raise ValidationError(_('Le numero de serie est encore valide:')+str(moves_lots.name))
    #         elif len(moves_lots)>1:
    #             for lot in moves_lots:
    #                 life_date_obj = datetime.datetime.strptime(lot.life_date, '%Y-%m-%d %H:%M:%S')
    #                 life_date = life_date_obj.date()
    #                 if (today_date < life_date):
    #                     raise ValidationError(_('Le numero de serie est encore valide:') + str(lot.name))

     @api.multi
     def action_done(self):
    
         res = super(StockPicking, self).action_done()
         self.checkLoc_LotAvailableQuant()   
           # raise ValidationError(_("L'emplacement source n'est pas un empl de stock valide svp (XXX/stock)"))
    
         return  res


    def checkLoc_LotAvailableQuant(self):

        reference=self.picking_type_code

        if reference in ['outgoing','internal'] :

            location_id = self.location_id.id
            #move_lines = self.move_lines
            move_lines = self.move_line_ids
            available_qty=0
            product_qty=0

            for mvl in move_lines:
                moves_lots=mvl.lot_id

                if len(moves_lots)==1:
                    available_qty=sum(q.quantity for q in self.env['stock.quant'].search(['&',('location_id','=',location_id),('lot_id','=',moves_lots.id)]))
                    product_qty=mvl.product_qty
                    if available_qty<0:
                        raise ValidationError(_('Le numero de lot :'+str(moves_lots.name)+'\tne contient pas assez de produits pour faire cette operation'+'\nBien vouloir verifier votre stock et choisir un autre lot au besoin\n Quantité en moins:\t'+str(abs(available_qty))))
                elif len(moves_lots)>1:
                    for lot in moves_lots:
                        available_qty=sum(q.quantity for q in self.env['stock.quant'].search(['&',('location_id','=',location_id),('lot_id','=',lot.id)]))
                        product_qty=mvl.product_qty
                        if (available_qty<0):
                            raise ValidationError(_('Le numero de lot :'+str(lot.name)+'\tne contient pas assez de produits pour faire cette operation'+'\nBien vouloir verifier votre stock et choisir un autre lot au besoin\n Quantité en moins:\t'+str(abs(available_qty))))


    @api.multi
    def button_validate(self):

        res = super(StockPicking, self).button_validate()
        #self.checkLoc_LotAvailableQuant()
        #raise ValidationError(_("L'emplacement source n'est pas un empl de stock valide svp (XXX/stock)---1"+self.picking_type_code))

        return  res

# class stock_immediat_transfer(models.TransientModel):
#     _name = 'stock.immediate.transfer'
#     _inherit = 'stock.immediate.transfer'
#
#
#     def process(self):
#         res = super(stock_immediat_transfer,self).process()
#
#
#         return res
