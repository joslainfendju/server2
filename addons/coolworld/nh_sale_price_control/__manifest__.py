# -*- coding: utf-8 -*-
{
    'name': "nh_sale_price_control",

    'summary': """
        This Module is to control sale price. You can't not decrease the sale price.""",

    'description': """
        This Module is to control sale price. You can't not decrease the sale price.
    """,

    'category': 'sale',
    'version': '11.0.0.0.1',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','nh_3n_pharma_sale_promotion_buyX_getY','product','nh_3n_pharma_sale_process'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/price_list.xml',
        'views/sale_order.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}