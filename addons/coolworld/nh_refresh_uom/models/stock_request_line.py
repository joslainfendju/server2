# -*- coding: utf-8 -*
#Bibliotheques pour le modèle
from odoo import models, fields, api, _
#pour les logs
import logging
_logger = logging.getLogger(__name__)


class StockRequestLine(models.Model):
    _inherit = 'nh_scm.stock_request_line'

    purchase_uom_id = fields.Many2one('product.uom', compute="_get_default_uoms")
    sale_uom_id = fields.Many2one('product.uom', compute="_get_default_uoms")

    @api.depends('product_id')
    def _get_default_uoms(self):
        for rec in self:
            rec.purchase_uom_id = rec.product_id.product_tmpl_id.uom_po_id
            rec.sale_uom_id = rec.product_id.product_tmpl_id.uom_id



    @api.onchange('product_id')
    def get_domain_uom(self):
       result = super(StockRequestLine, self).get_domain_uom()


       if (self.product_id and 'domain' in result and 'product_uom_id' in result['domain']):
           if not 'value' in result:
               result.update({'value': {}})

           result['value'].update({'product_uom_id': self.product_id.product_tmpl_id.uom_id.id})
           result['domain'].update({'product_uom_id': [('id', 'in', [self.product_id.product_tmpl_id.uom_id.id,
                                                                  self.product_id.product_tmpl_id.uom_po_id.id])]})

       return result




