# -*- coding: utf-8 -*-

{
    'name': "nh_3n_pharma_sale_promotion",
    'version': '0.1',
    'summary': """Create Promotion Offers For Sales""",
    'description': """This Module Allows to Set  Promotion Offers On Products And Product Categories.""",
    'author': "NH-IT",
    'website': "https://www.nh-itc.com",
    'category': 'Sales',
    'depends': ['sale', 'account_invoicing','branch'],
    'data': [
        'security/ir.model.access.csv',
        'views/promotion_product.xml',
        'views/sale_promotion_rule.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'auto_install': False,
}


