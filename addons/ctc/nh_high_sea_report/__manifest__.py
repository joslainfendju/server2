# -*- coding: utf-8 -*-
{
    'name': "nh_high_sea_report",

    'summary': """
       L'objectif de ce module est de vous permettre d'avoir une vue détaillée du stock en mer.
       Le rapport vous permet en outre d'avoir le nombre de jours de retard pour chaque commande.
       Les rapports sont disponible sous EXCEL et PDF.
       L'analyse se fait par  produits/catégories.
       """,

    'description': """
       L'objectif de ce module est de vous permettre d'avoir une vue détaillée du stock en mer.
       Le rapport vous permet en outre d'avoir le nombre de jours de retard pour chaque commande.
       Les rapports sont disponible sous EXCEL et PDF.
       L'analyse se fait par  produits/catégories.
    """,

    'author': "NH-IT",
    'website': "http://www.its-nh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '11.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','nh_3n_pharma_land_cost'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'report/high_sea_report_layout.xml',
        'report/high_sea_report_template.xml',
        'wizard/high_sea_transit_report_wizard.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}