# -*- coding: utf-8 -*-
{
    'name': "its_voucher_type_on_report",

    'summary': """
        The role of this module is to include the voucher type in ledger report
        """,

    'description': """
         The role of this module is to include the voucher type in ledger report
    """,

    'author': "ITS",
    'website': "http://www.its.itc-nh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Account',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','account_reports','its_bank_register'],

    # always loaded
    'data': [
        # 'security/ir.models.access.csv',
        #'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}