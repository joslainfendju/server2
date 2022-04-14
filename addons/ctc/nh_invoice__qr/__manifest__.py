# -*- coding: utf-8 -*-
{
    'name': "nh_invoice_QR",

    'summary': """
        Ce Module permet d'ajouter les codes QR sur les factures, sur les bons de commandes et sur les bons de livraisons.""",

    'description': """
        Ce Module permet d'ajouter les codes QR sur les factures, sur les bons de commandes et sur le bon de livraison.
        Le code QR contient la réference du document, le montant total et le nom du client.
    """,

    'author': "NH-IT",
    'website': "http://www.its-nh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}