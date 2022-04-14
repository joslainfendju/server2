  # -*- coding: utf-8 -*-
{
    'name' : 'nh_3n_internal_transfert',
    'version' : '1.0',
    'author' : 'NH-ITS',
    'sequence': 2,
    'description' : 'module qui ajoute la contrainte de la validtion DG sur les transferts interne',
    'category': 'Enterprise Innovation',
    'website': 'http://www.nh-its.com',
    'depends' : ['base','stock','nh_scm'],
    'data' : [ 
                'views/stock_picking_view.xml',
                'security/security.xml'
                

             ],
   
	
	'installable': True,
	'application': False,
	'auto_install': False,
}