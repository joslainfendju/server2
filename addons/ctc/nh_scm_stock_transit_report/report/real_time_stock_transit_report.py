#!/usr/bin/env python
# -*- coding:utf-8 -*-

##############################################################################
#
#
##############################################################################


from odoo import api, fields, models
from openerp.api import Environment as Env
import logging
import datetime


class RealTimeTransitReport(models.AbstractModel):
    _name = 'report.nh_scm_stock_transit_report.report_transit'

    @api.model
    def render_html(self, docids, data=None):
        docargs = {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['elements'],
            'branch_src_id': data['branch_src_id'],
            'branch_dest_id': data['branch_dest_id'],
            'specific_date': data['specific_date'],

        }
        return self.env['report'].render('nh_scm_stock_transit_report.report_transit', docargs)

    @api.multi
    def get_report_values(self, docids, data=None):


        docargs = {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['elements'],
            'branch_src_id': data['branch_src_id'],
            'branch_dest_id': data['branch_dest_id'],
            'specific_date': data['specific_date'],

        }
        return docargs




