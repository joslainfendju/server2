# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo NH-IT
#    Copyright (C) 2018 NH-IT (<http://www.its-itc.com>).
#
##############################################################################
import time
from datetime import datetime
from dateutil import relativedelta
import itertools
from operator import itemgetter
import operator

from datetime import datetime, timedelta
from odoo import api, models


class stock_transit_report(models.AbstractModel):
    _name = 'report.nh_scm_stock_transit_report.report_template'


    @api.multi
    def get_warehouse_data(self, data):
        return data

    @api.multi
    def get_wizard_data(self, data):
        return data

    @api.multi
    def get_transit_move_lines(self, products, branch_src=None, branch_dest=None, direction='any', data=None):
        state = 'done'
        start_date = str(data.start_date) + ' 00:00:00'
        end_date = str(data.end_date) + ' 23:59:59'
        moves = []

        base_domain = ['&', ('state', '=', state), '&', ('product_id', 'in', [p.id for p in products]),
                       '&', ('date', '>=', start_date), ('date', '<=', end_date)
                       ]
        if branch_src:
            move_line_ids = self.env['stock.move.line'].search(
                ['&', ('move_id.picking_id.origin', '!=', False), '!', ('location_id.branch_id', '=', branch_src.id)])
            line_ids = []
            for line in move_line_ids:
                pick = self.env['stock.picking'].search([('name', '=', line.move_id.picking_id.origin)])
                if pick and pick.branch_id.id == branch_src.id:
                    line_ids.append(line.id)
            if line_ids:
                base_domain = ['&', '|', ('location_id.branch_id', '=', branch_src.id),
                               ('id', 'in', line_ids)] + base_domain
            else:
                base_domain = ['&', ('location_id.branch_id', '=', branch_src.id)] + base_domain

        if branch_dest:
            base_domain = ['&', ('location_dest_id.branch_id', '=', branch_dest.id)] + base_domain
        if direction == 'any':
            base_domain = ['&', '|', ('location_dest_id.usage', '=', 'transit'),
                           ('location_id.usage', '=', 'transit')] + base_domain
        elif direction == 'incoming':

            base_domain = ['&', ('location_dest_id.usage', '=', 'transit')] + base_domain
        else:
            base_domain = ['&', ('location_id.usage', '=', 'transit')] + base_domain

        return self.env['stock.move.line'].search(base_domain)


    def get_product(self, data):
        product_pool = self.env['product.product']
        if not data.filter_by:
            product_ids = product_pool.search([('type', '!=', 'service')])
            return product_ids
        elif data.filter_by == 'product' and data.product_ids:
            return data.product_ids
        elif data.filter_by == 'category' and data.category_id:
            product_ids = product_pool.search(
                [('categ_id', 'child_of', data.category_id.id), ('type', '!=', 'service')])
            return product_ids



    @api.multi
    def get_lines(self, data):

        res = []
        move_lines = self.get_transit_move_lines(self.get_product(data), data.branch_src_id, data.branch_dest_id,
                                                 data.direction,data)
        for line in move_lines:
            request = ""
            if line.move_id and line.move_id.picking_id:
                if line.move_id.picking_id.request_id:
                    request = line.move_id.picking_id.request_id.name
                elif line.move_id.picking_id.receipt_from_request_id:
                    request = line.move_id.picking_id.receipt_from_request_id.name
                elif line.move_id.picking_id.return_request_id:
                    request = line.move_id.picking_id.return_request_id.name
                elif line.move_id.picking_id.receipt_from_return_request_id:
                    request = line.move_id.picking_id.receipt_from_return_request_id.name
            picking = "Undefined"
            if line.move_id and line.move_id.picking_id:
                picking = line.move_id.picking_id.name

            direction = ""
            if line.location_dest_id.usage == 'transit':
                direction = 'Incoming to transit'
            else:
                direction = 'Leaving to transit'

            vals = {
                'date': line.move_id.picking_id.write_date,
                'code': line.product_id.code,
                'product': line.product_id.product_tmpl_id.name,
                'lot': line.lot_id.name,
                'uom': line.product_uom_id.name,
                'request': request,
                'picking': picking,
                'location_id': line.location_id.display_name,
                'location_dest_id': line.location_dest_id.display_name,
                'direction' : direction,
                'qty': line.qty_done,
                'value': line.product_id.uom_po_id._compute_quantity(line.qty_done, line.product_uom_id,
                                                                               rounding_method='HALF-UP') * line.product_id.standard_price,
            }



            res.append(vals)
        return res


    @api.multi
    def get_report_values(self, docids, data=None):
        docs = self.env['nh_scm_stock_transit_report.data_wizard'].browse(data['form'])
        return {
            'doc_ids': docs.ids,
            'doc_model': 'nh_scm_stock_transit_report.data_wizard',
            'docs': docs,
            'proforma': True,
            #'get_warehouse_data': self.get_warehouse_data(docs.warehouse_id),
            'get_wizard_data': self.get_wizard_data(docs),
            'get_lines': self.get_lines(docs)
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
