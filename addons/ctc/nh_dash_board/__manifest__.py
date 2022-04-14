# -*- coding: utf-8 -*-
{
    'name': "nh_dash_board",

    'summary': """
       Ce module vous permet d'avoir un resumé de vos activités sous forme de graphique.""",

    'description': """
        Ce module vous permet d'avoir un resumé de vos activités sous forme de graphique.
        Il vous donne les resumés suivants:
        - détails des ventes
        - détails des paiements
        - détail d'aprrovisionnement
        - détails d'achats
        - la liste des clients endettés
        - la valorisation du stock
    """,

    'author': "NH-IT",
    'website': "http://www.its-nh.com",
    'application' :True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','branch','stock','nh_3n_pharma_land_cost','nh_scm','account'],

    # always loaded
    'data': [

        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/nh_dash_board.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}