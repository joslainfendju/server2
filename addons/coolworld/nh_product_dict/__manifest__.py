# -*- coding: utf-8 -*-
{
    'name': "nh_product_dict",

    'summary': """
        Ce module ajoute un attribut famille sur la fiche du produit. et Veille à ceque:
        - par défaut la méthode de valuation doit être "real time"
        - les articles stockables doivent être automatiquement traquées par lots
        - la facturation soit basée sur qté reçues et livrées
        """,

    'description': """
        - par défaut la méthode de valuation doit être "real time"
        - les articles stockables doivent être automatiquement traquées par lots
        - la facturation soit basée sur qté reçues et livrées
    """,

    'author': "NH-IT/Patrick Tzorneu",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Product',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
        'purchase',
        'stock_account'
    ],

    # always loaded
    'data': [
        # security
        'security/ir.model.access.csv',

        # views
        'views/product_family_view.xml',
        'views/product_category_view.xml',
        'views/product_template_view.xml',
        'views/product_uom_view.xml',
        'views/action_view.xml',
        'views/menu_view.xml',
    ],

}