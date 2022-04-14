# -*- coding: utf-8 -*-
{
    'name': "nh_3n_pharma_land_cost",

    'summary': """
        Ce module permet de gérer le workflow des achats par importation tout en intégrant les calculs des côuts de revients.
        """,

    'description': """
        Ce module permet de gérer le workflow des achats par importation tout en intégrant les calculs des côuts de revients.
        Après Création d'un devis brouillon, il faut une confirmation de la commande.
        Après confirmation de la commande, le passage en production indique que le fournisseur a lancé la fabrication.
        En outre, une fois que les articles commandés sont embarqués il ne reste plus qu'à passer en transit.
        Après le passage en transit, les articles arrivent au port. Il ne reste plus qu'à renseigner les différents frais de transit.
        Une fois le renseignement des frais ok, lancer le calcul des coûts de revient.
        Une fiche de calcul peut être approuvée ou rejettée. La validation d'une fiche de calcul de coût induit la création du bon de réception et
        la fixation des ooûts de revient dans le système.
        La journalisation des coûts de revient est visible sur la fiche du produit et sur les lignes de mouvements de stock.
    """,

    'author': "NH-IT",
    'website': "https://www.nh-itc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '11.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'product', 'stock_account', 'branch', 'board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order.xml',
        'views/land_cost.xml',

        'views/product_template.xml',
        'wizard/land_cost_confirmation.xml',
        'wizard/land_cost_export.xml',
        'data/ir_sequence_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}