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
    _name = 'report.nh_high_sea_report.report_transit'



    @api.multi
    def get_report_values(self, docids, data=None):


        docargs = {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['elements'],
            'country_src_id': data['country_src_id'],
            'country_dest_id': data['country_dest_id'],
            'specific_date': data['specific_date'],

        }
        return docargs




