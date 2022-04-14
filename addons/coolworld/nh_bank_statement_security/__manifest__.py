
# -*- coding: utf-8 -*-
{
    'name': "nh_bank_statement_security",

    'summary': """
        This module is for adapt odoo for the mobile system SFA interconnection""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ITS",
    'website': "http://www.its-nh.com",
    'application' :True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['its_voucher_type_on_report', 'branch'],

    # always loaded
    'data': [
        'views/account_bank_statement_view.xml',
        'views/account_journal_view.xml',
        'security/journal_security.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
