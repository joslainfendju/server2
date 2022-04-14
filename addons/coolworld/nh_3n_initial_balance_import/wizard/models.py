# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import base64
from xlrd import open_workbook
import logging
from openerp.exceptions import ValidationError


class Intial_balance(models.TransientModel):
    _name = 'initial.balance.load'

    account_move_id = fields.Many2one('account.move', 'Piece d\'ouverture')
    data = fields.Binary('File',help="select field that content initial account_entries")
    filename = fields.Char('File Name', required=True)

    def _find_partner_by_name(self,name):
         res=self.env['res.partner'].search([('name','=',name)])
         if len (res)==0:
             raise ValidationError(_("Partner  '%s' not found")%(name))
         elif len(res)>1:
             raise ValidationError(_("Partner  '%s' found twice") % (name))

         return res.id

    def _find_account_by_code(self, code):
        res = self.env['account.account'].search([('code', '=', code)])
        if len(res)== 0:
            raise ValidationError(_("Account  '%s' not found") % (code))
        elif len(res) > 1:
            raise ValidationError(_("Account  '%s' found twice") % (code))

        return res.id

    def load_init_balance(self):
        move_id = self.account_move_id

        #partner_id=self._find_partner_by_name(partner)
        wb = open_workbook(file_contents=base64.b64decode(self.data))
        sheet = wb.sheet_by_index(0)
        number_of_rows = sheet.nrows
        datop=self.account_move_id.date
        journal_id=self.account_move_id.journal_id.id
        account_dic=dict()
        account_dic.update({
            'line_ids':[]
        }
        )

        for row in range(0, number_of_rows):
            compte=str(sheet.cell(row, 0).value)
            debit = sheet.cell(row, 1).value or 0.0
            credit = sheet.cell(row, 2).value or 0.0
            account_id =self._find_account_by_code(compte[:-2])

            mvl_json={
                'account_id':account_id,
                'credit':credit,
                'debit':debit,
                'date':datop,
                'date_maturity':datop,
                'move_id':move_id.id,
                'journal_id':journal_id
            }
            account_dic['line_ids'].append((0,0,mvl_json))
        move_id.write(account_dic)














            # sql = "INSERT INTO account_move_line (account_id,credit,debit,date,date_maturity,move_id,journal_id) VALUES (%s, %s, %s, %s, %s, %s,%s)"
            #
            # val=(account_id,credit,debit,datop,datop,move_id,journal_id)
            # self.env.cr.execute(sql,val)







