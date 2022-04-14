# Copyright 2016 Akretion (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'NH 3N report update',
    'version': '11.0.1.0.0',
    'category': '',
    'license': 'AGPL-3',
    'summary': "Adds as buttons category",
    'author': "ITS-NH",
    'website': 'its-nh.com',
    'depends': ['base','nh_3n_pharma_sale_promotion_buyX_getY','stock'],
    'data': [
        'views/invoice.xml',
        'views/delivery_order.xml'
    ],
    'installable': True,
}
