# -*- coding: utf-8 -*-
{
    'name': "nh_scm_stock_transit_report",

    'summary': """
       L'objectif de ce module est de vous permettre d'avoir une vue détaillée du stock en transit.
       Les rapports sont disponible sous EXCEL et PDF.
       L'analyse se fait par société, branches,produits/catégories.
       """,

    'description': """
       L'objectif de ce module est de vous permettre d'avoir une vue détaillée du stock en transit.
       Les rapports sont disponible sous EXCEL et PDF.
       L'analyse se fait par société, branches,produits/catégories.
    """,

    'author': "NH-IT",
    'website': "http://www.its-nh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '11.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','branch','nh_scm','web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'report/transit_history_layout.xml',
        'report/transit_history_report_template.xml',
        'wizard/stock_transit_history_report_wizard.xml',
        'report/real_time_stock_transit_report_template.xml',
        'wizard/real_time_stock_transit_report_wizard.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}