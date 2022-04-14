# -*- coding: utf-8 -*-
{
    'name': "nh_move_stock_patch",

    'summary': """
        This module makes it possible to make the _account_entry_move method public""",

    'description': """ """,

    'author': "ITS, Thierry TJAMACK",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'stock_account',
    ],

    # always loaded
    'data': [
        'wizard/wizard_account_move_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}