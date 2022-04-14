# -*- coding: utf-8 -*-
{
    'name': "nh_3n_pharma_sale_process",

    'summary': """
        The role of this module is to apply 3N Pharma workflow of sale.""",

    'description': """
        The role of this module is to apply 3N Pharma workflow of sale.
    """,

    'author': "NH-IT",
    'website': "http://www.its-nh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'sale',
    'version': '11.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock','branch'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/sale_order_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}