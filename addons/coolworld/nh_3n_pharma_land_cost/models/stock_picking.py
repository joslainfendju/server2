# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
import datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"
    _name = 'stock.picking'

    @api.multi
    def check_if_there_is_an_unreceived_order_from_fixed_land_cost(self):
        """
            Vérification s'il n'existe pas de fiche de calcul de coût validée et dont les réceptions ne sont pas ok
            pour ce cas, tous les autres mouvements sauf la réception elle même doit pouvoir être validée
        """

        land_costs_saved_without_receipt = self.env['nh_3n_pharma_land_cost.land_cost'].search(
            ['&', ('order_id.type', '=', 'abroad'), '&', ('state', '=', 'approved'),
             ('order_id.state', '=', 'cost_saved')])

        # récupération des produits concernés par les achats
        products_in_danger = []
        for land in land_costs_saved_without_receipt:
            purchase_order = land.order_id
            all_processed = True
            for picking in purchase_order.picking_ids:
                if picking.picking_type_id.code == "incoming" and picking.state not in ('done', 'cancel',):
                    all_processed = False
            if not all_processed:
                for line in purchase_order.order_line:
                    if line.product_id.id not in products_in_danger:
                        products_in_danger.append(line.product_id.id)

        # Analyse du document de livraison et/ou interne en cas de validation
        if self.picking_type_id.code != 'incoming':
            for line in self.move_lines:
                if line.product_id.id in products_in_danger:
                    raise UserError(_("You need to receive %s relatively to an abroad purchase (for update cost price) before doing this operation"%line.product_id.product_tmpl_id.display_name))



    @api.multi
    def update_cost_price_after_receiving_import_purchase(self):
        if self.picking_type_id.code == "incoming":
            is_a_land_cost_purchase = False
            for line in self.move_lines :
                if  line.purchase_line_id:
                    old_cost_price = line.product_id.standard_price

                    land_cost_line = self.env['nh_3n_pharma_land_cost.land_cost_line'].search(['&',('purchase_order_line_id','=',line.purchase_line_id.id),('land_cost_id.state','in',('approved',))])

                    if land_cost_line:
                        is_a_land_cost_purchase = True

                        line.product_id.write(
                            {
                                # 'standard_price': line.cost_price_after_purchase ,
                                'standard_price': land_cost_line.cost_price_after_purchase,
                            }
                        )
                        self.env['nh_3n_pharma_land_cost.land_cost_log'].create(
                            {
                                'land_cost_id': land_cost_line.land_cost_id.id,
                                'land_cost_line_id': land_cost_line.id,
                                'product_template_id': line.product_id.product_tmpl_id.id,
                                'old_product_qty': land_cost_line.stock_before_arrival,
                                'old_product_cost': old_cost_price,
                                'landed_product_qty': land_cost_line.purchase_qty,
                                'landed_product_cost': land_cost_line.global_cost_purchase,
                                # 'new_product_cost': line.product_id.standard_price,
                                'new_product_cost': land_cost_line.product_id.standard_price,
                                'date_log': fields.Datetime.now(),
                            }
                        )
            #s'il s'agit d'une réception de land cost, alors faut mettre à jour l'état du bon de commande d'achat
            #Celui-ci doit être à l'état "terminé" si tous les bons ont été reçu.
            if is_a_land_cost_purchase:
                purchase_order = self.purchase_id
                all_processed = True
                for picking in purchase_order.picking_ids:
                    if picking.picking_type_id.code == "incoming" and picking.state not in ('done', 'cancel',):
                        all_processed = False

                #Nous sommes dans le cas pour lequel toutes les réceptions ont été faites
                if all_processed:
                    purchase_order.write({
                        'state': 'done',
                        'date_done': fields.Datetime.now()
                    })




    @api.multi
    def action_done(self):

        """vérifions d'abord s'il n'existe pas un bon de réception en attente issu d'un achat à l'étranger.
        Dans ce cas, la réception doit être faite avant toute livraison ou transfert interne
        """
        self.check_if_there_is_an_unreceived_order_from_fixed_land_cost()

        """ exécution du transfert, le cas pour lequel il n'y a pas de contrainte"""
        res = super(StockPicking, self).action_done()
        """fin exécution du transfert"""

        #Après le transfert, il faut maintenant positionner le Coût Unitaire Moyen Pondéré (CUMP) pour le cas des achats avec Land Cost
        #Ce cas s'applique seulement pour les bons de réception
        self.update_cost_price_after_receiving_import_purchase()