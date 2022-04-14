# -*- coding: utf-8 -*-
{
    'name': "nh_3n_pharma_periodic_expirer_alert",

    'summary': """
       This module function is to send report about products'serial number out to expire in the system.""",

    'description': """
        This module function is to send report about products'serial number out to expire in the system.
    """,

    'author': "NH-IT",
    'website': "https://www.nh-itc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','nh_alert_contact','branch'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'data/parametres_systeme.xml',
        'data/agent_rapporteur_perimes.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}