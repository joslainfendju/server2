# -*- coding: utf-8 -*-
{
    'name': "nh_3n_pharma_customer_supplier_infos",

    'summary': """Modifications on the data dictionaries of customer and supplier """,

    'description': """
        This module adds some fields to the data dictionaries of customer and supplier
    """,

    'author': "NH-IT",
    'website': "https://www.nh-itc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'branch'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/partner.xml',
        'demo/data.xml',
        'data/sequences.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/data.xml',
    ],
}