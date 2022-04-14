# -*- coding: utf-8 -*-
{
    'name': "nh_3n_pharma_sale_process_credit_limit",

    'summary': """
        Ce module permet de créer un pont entre le module de limite de crédit et celui de vente.
        L'objectif est ramener le contrôle de la limite de crédit au premier niveau de validation.
        En outre l'on personnalise les messages d'erreurs en fonction du type de client.
        
        """,

    'description': """
        Ce module permet de créer un pont entre le module de limite de crédit et celui de vente.
        L'objectif est ramener le contrôle de la limite de crédit au premier niveau de validation.
    """,

    'author': "NH-IT",
    'website': "http://www.its-nh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sale',
    'version': '11.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','nh_3n_pharma_sale_process','nh_3n_pharma_credit_limit', 'nh_3n_pharma_customer_supplier_infos'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'data': [
        'data/error_message.xml',
    ],
}