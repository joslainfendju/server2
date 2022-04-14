# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

class  stock_picking(models.Model):
    _name= 'stock.picking'
    _inherit='stock.picking'


    validation_dg=fields.Char('Validation-dg',defaults='no_required')

    @api.model
    def create(self,vals):
        logging.info("DG VALidation %s"%(str(vals)))
        obj_stock_location=self.env['stock.location']
        dest_location=obj_stock_location.browse(vals['location_dest_id'])
        location = obj_stock_location.browse(vals['location_id'])
        if (dest_location.branch_id  and location.branch_id  and not location.branch_id.is_office_branch
                and  ((not 'request_id' in vals and not 'return_request_id' in vals)  or ( 'request_id' in vals  and not vals['request_id'] or  'return_request_id' in vals
                and not vals['return_request_id']))
               ):

            #On évite d'inclure la validation DG pour les transferts dans la même branche.
            if(dest_location.branch_id.id != location.branch_id.id and not dest_location.branch_id.is_office_branch):
                vals["validation_dg"]="required"

        return super(stock_picking,self).create(vals)

    def button_validate(self):

        obj_stock_picking=self.env['stock.picking']
        picking=obj_stock_picking.browse(self.id)

        if(picking.validation_dg=="required"):
            raise ValidationError(_("Une validation du DG est requise pour la suite du process"))
        return super(stock_picking,self).button_validate()

    def transfert_dg_validation(self):
            self.write({"validation_dg":'ok' })
            return True
