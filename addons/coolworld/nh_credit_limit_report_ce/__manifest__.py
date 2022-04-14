# -*- coding: utf-8 -*-
{
    'name': "nh_credit_limit_report_ce",

    'summary': """
        This module help you to print customers credit limits and condition of payment report on PDF.
        EXCEL format are also available for this type of report.
        You can  specify a branch for just print customers of this branch.
        """,

    'description': """
       This module help you to print customers credit limits and condition of payment report on PDF.
        EXCEL format are also available for this type of report.
        You can  specify a branch for just print customers of this branch.
    """,

    'author': "NH-IT",
    'website': "http://www.its-nh.com",
    
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Extra tools',
    'version': '11.0.0.0.0',


    # any module necessary for this one to work correctly
    'depends': ['base','nh_3n_pharma_credit_limit','account','branch','web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'modal/boite_dialogue.xml',
        'report/report_credit_limit.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}