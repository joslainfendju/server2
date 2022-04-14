# -*- coding: utf-8 -*-
{
    'name': 'Hr Expense Flexible Approval Process',
    'version': '1.0.01',
    'summary': """
    Dynamic, Customizable and flexible approval cycle for expenses
    | purchase approval 
    | expense approval process
    | Expense approval cycle 
    | Expense approval process
    | Expense approval workflow
    | approve Expense
    | approve Expense
    """,
    'category': 'Hr',
    'author': 'Patrick Tzorneu',
    'support': 'pole.si@nh-itc.com',
    'website': 'https://www.its-nh.com',
    'license': 'OPL-1',
    'price': 10,
    'currency': 'EUR',
    'description':
        """
Expense Approval Cycle
=============================
This module helps to create multiple custom, flexible and dynamic approval route
for expenses based on Expense Team settings.

Key Features:

 * Purchase Manager can configure unlimited expense approval process rules by creating Expense Teams
 * Approval Cycle can be generated dynamically based on Total Amount of expense
 * expense Approval Process can be used optionally or forcibly, depending on the module settings
 * Locking Total Amount of expense after receiving approval from particular approver or after finishing approval flow
 * Unlimited level of "step by step" approval
 * Multi Company and Multi Currency features of Odoo System are supported
 
        """,
    'data': [
        'security/ir.model.access.csv',
        'security/hr_expense_security.xml',
        'data/hr_expense_approval_route.xml',
        'views/expense_approval_route.xml',
        'views/res_config_settings_views.xml',
    ],
    'depends': ['purchase', 'hr_expense'],
    'qweb': [],
    'images': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
