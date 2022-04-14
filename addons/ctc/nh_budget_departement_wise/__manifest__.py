# -*- coding: utf-8 -*-
{
    'name': "Budget Departement Wise",

    'summary': """
        Duplicate Voucher: - Voucher with Same amount, date, reference, account, department wise, 
        tag, analytical account, - all this must be control during recording and must alert if user did not fill 
        the detail correctly or entry has been pass double with same detail .
        Any expenses voucher or P.O. should not be created without selecting department wise expenses, analytical account and tag
        Expenses should come department wise – inside that analytical account then tag account. 
        """,


    'description': """
        Duplicate Voucher: - Voucher with Same amount, date, reference, account, department wise, 
        tag, analytical account, - all this must be control during recording and must alert if user did not fill 
        the detail correctly or entry has been pass double with same detail .
        Any expenses voucher or P.O. should not be created without selecting department wise expenses, analytical account and tag
        Expenses should come department wise – inside that analytical account then tag account. 
    """,

    'author': "ITS Sarl",
    'website': "http://its-nh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Account',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_invoicing', 'branch', 'nh_budget_managment_ce'],

    # always loaded
    'data': [
        # 'security/ir.models.access.csv',
        'views/account_bank_statement.xml',
        'views/account_move_line.xml',
        'views/account_analytic_line.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}