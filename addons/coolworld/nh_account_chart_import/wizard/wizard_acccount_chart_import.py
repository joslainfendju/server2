from odoo import fields, models, api,_
import logging
from xlrd import open_workbook
import base64
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class AccountChartImport(models.TransientModel):
    _name ="nh.account.chart.import"

    data = fields.Binary('Account chart file')
    file_name = fields.Char('File name')

    @api.multi
    def action_import(self):
        datas = self.data
        wb = open_workbook(file_contents=base64.b64decode(datas))
        sheet = wb.sheet_by_index(0)
        number_of_rows = sheet.nrows
        vals = {}
        account_obj = self.env["account.account"]
        account_group_obj = self.env["account.group"]
        for row in range(1, number_of_rows):
            code = str(int(float(sheet.cell(row, 0).value)))
            name = sheet.cell(row, 1).value

            is_group = sheet.cell(row, 2).value == "True"

            if not name or name == '' or not code or code == '':
                raise ValidationError('Name undefined!!!\n Please name or code is required at line '+str(row))
            if is_group:
                group = account_group_obj.search([('code_prefix', '=', code)])
                if group:
                    group.write({'name': name})
                else:
                    group = account_group_obj.create({'code_prefix': code, 'name': name})
                parent = group.search_real_parent()
                if parent:
                    group.write({'parent_id': parent.id})
            else:
                type_id = int(float(sheet.cell(row, 3).value))
                account = account_obj.search([('code', '=', code)])
                reconcile = sheet.cell(row, 4).value == "True"
                if account:
                    account.write({'name': name, 'user_type_id': type_id, 'reconcile': reconcile})
                else:
                    account = account_obj.create({'code': code, 'name': name,
                                                  'user_type_id': type_id,
                                                  'reconcile': reconcile,
                                                 })
                    account.write({
                        'user_type_id': type_id,
                        'reconcile': reconcile
                    })
                group = account.search_group()
                if group:
                    account.write({'group_id': group.id})
        return True







