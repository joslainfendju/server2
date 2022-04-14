# -*- coding: utf-8 -*-
{
    'name': "nh_alert_contact",

    'summary': """
        This module is to define a framework for contact to alert in any odoo module.""",

    'description': """
        This module is to define a framework for contact to alert in any odoo module.
    """,

     'author': "NH-IT",
    'website': "https://www.nh-itc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Settings',
    'version': '11.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','branch'],

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