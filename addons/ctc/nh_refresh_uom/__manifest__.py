{
    'name' : 'NH-REFRESH UOM',

    'version' : '11.0.0.1',
    'author' : 'NH-IT',
    'description' : 'Ce module peremt d\'actualiser les unités de mésures sur les bons d\'achats et de ventes après changement de l\'article',
    'category': 'Recherche et developpement',
    'website': 'http://www.nh-itc.com',
    'depends' : ['base', 'purchase','sale', 'nh_scm'], # liste des dépendances

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'view/purchase_order.xml',
        'view/sale_order.xml',
        'view/stock_request.xml',
        'view/return_request.xml',
        'view/purchase_indent.xml',
        'view/internal_reorder_parameter.xml',
        'view/external_reorder_parameter.xml',




    ],
    
}