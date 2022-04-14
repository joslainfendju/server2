# -*- coding: utf-8 -*
#Bibliotheques pour le modèle
from odoo import models, fields, api , _
#pour les logs
import logging
_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'


    purchase_uom_id = fields.Many2one('product.uom' , compute="_get_default_uoms")
    sale_uom_id = fields.Many2one('product.uom' , compute="_get_default_uoms")

    @api.depends('product_id')
    def _get_default_uoms(self):
        for rec in self:
            rec.purchase_uom_id = rec.product_id.product_tmpl_id.uom_po_id
            rec.sale_uom_id = rec.product_id.product_tmpl_id.uom_id

    @api.onchange('product_id')
    def onchange_product_id(self):

        result = super(PurchaseOrderLine, self).onchange_product_id()
        if(self.product_id  and 'domain' in result and 'product_uom' in result['domain'] ):
            result['domain'].update({'product_uom':[('id','in',[self.product_id.product_tmpl_id.uom_id.id , self.product_id.product_tmpl_id.uom_po_id.id])]})
            if not 'value' in result:
                result.update({'value' : {}})
            result['value'].update({'product_uom': self.product_id.product_tmpl_id.uom_id.id})

        return result

