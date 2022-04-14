# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import re
import logging
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _name = 'stock.move.line'
    _inherit = 'stock.move.line'

    sequence_numbers = fields.Char("Sequence Numbers")

    @api.constrains('sequence_numbers')
    def check_constraint(self):
        pattern_plage = "^(\d+\-\d+)$"
        pattern_liste = "^\d+(;\d+)*$"
        if  self.sequence_numbers and self.sequence_numbers != '':
         if not re.match(pattern_liste , self.sequence_numbers) and not re.match(pattern_plage , self.sequence_numbers):
             raise UserError(_("Sequences Number Must be in the format First-Last or number;number2;...;number N "))

         else :
             if re.match(pattern_plage , self.sequence_numbers):
                 interval = self.sequence_numbers.split('-')
                 if int(interval[0]) > int(interval[1]):
                     raise UserError(_("In case of an interval, the minimun must be less than the maximun."))



