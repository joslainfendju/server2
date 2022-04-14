# See LICENSE file for full copyright and licensing details.

{
    'name': 'nh_3n_pharma_credit_limit',
    'version': '11.0.1.0.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'author': 'Tiny, Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'summary': 'Set credit limit warning',
    'depends': [
        'sale_management','branch','base',
    ],
    'data': [
        'views/partner_view.xml',
        #'security/security.xml',
        'data/parametres_systeme.xml',
    ],
    'installable': True,
    'auto_install': False,
}
