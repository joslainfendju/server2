#!/usr/bin/env python
#-*- coding:utf-8 -*-

##############################################################################
#
#
##############################################################################


from odoo import api, fields, models
from openerp.api import Environment as Env
import logging



class ReportCreditLimit(models.AbstractModel):
    _name = 'report.nh_credit_limit_report.report_credit_limit'

    @api.model
    def render_html(self, docids, data=None):
        docargs =  {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['elements'],
            'branch_id': data['branch_id'],
            
        }
        return self.env['report'].render('nh_credit_limit_report.report_credit_limit', docargs)

    @api.multi
    def get_report_values(self, docids, data=None):
        docargs =  {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['elements'],
            'branch_id': data['branch_id'],
            
        }
        return docargs

        
        

