# -*- coding: utf-8 -*-
{
    'name': "nh_3n_initial_balance_import",

    'summary': """
      """,

    'description': """
       
    """,

    'author': "NH-IT",
    'website': "https://www.nh-itc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock', 'branch',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/init_balance.xml',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}