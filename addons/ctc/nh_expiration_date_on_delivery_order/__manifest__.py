# -*- coding: utf-8 -*-
{
    'name': "nh_expiration_date_on_delivery_order",

    'summary': """
        This module role is to add the expiration date on the delivery order.""",

    'description': """
        This module role is to add the expiration date on the delivery order.
    """,

    'author': "NH-IT",
    'website': "http://www.its-nh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account'],

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