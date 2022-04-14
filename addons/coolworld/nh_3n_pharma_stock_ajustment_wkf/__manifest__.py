# -*- coding: utf-8 -*-
{
    'name': "nh_3n_pharma_stock_ajustment_wkf",

    'summary': """
       Ce module permet d'inclure deux niveaux de validations dans le processus d'ajustement de stock.
       En outre ce module protège tous les boutons de ce menu dans des groupes de sécurités.
       """,

    'description': """
        Ce module permet d'inclure deux niveaux de validations dans le processus d'ajustement de stock.
       En outre ce module protège tous les boutons de ce menu dans des groupes de sécurités.
    """,

    'author': "NH-IT",
    'website': "https://www.nh-itc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_inventory.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}