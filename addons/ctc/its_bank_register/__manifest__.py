# -*- coding: utf-8 -*-
{
    'name': "Its bank Register",

    'summary': """
        This module purpose is to help you to record in a single register, all your bank account
        statment lines. It also provide a feature for record all your transaction type (voucher type).""",

    'description': """
        User should be able to select the VOUCHER TYPE or automate the same based on the
        screen/interface, so that the user can pass the transaction respective to the transaction being
        recorded. For example, the user can select the BANK ACCOUNT for the Bank deposits done
        by the customers.
        The TRANSACTION TYPE can be as follows: BANK Receipt, Cash Receipt, BANK
        CHEQUE Receipt, BANK TRANSFER, Contra Voucher, CASH Payment, Bank Cheque
        Payment)
        1. Select the Voucher type as per transaction purpose or automate the same based on the
        screen/interface.
        2. Select the Account name related to Bank or Cash, Receivable or Payable Account or
        Expenses Account and then Select Debit or Credit.
        3. Should be able to pass one entry for each transaction by Selecting two account – One
        Credit and one Debit.
        4. We should be able to reconciled each bank/account in ERP and able to See voucher type
        in respective Account Ledger as per attached sheet
    """,

    'author': "ITS Sarl",
    'website': "http://its.nh-itc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Account',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_invoicing', 'account_reports', 'branch'],

    # always loaded
    'data': [
        # 'security/ir.models.access.csv',
        'views/account_journal_dashboard_view.xml',
        'views/account_bank_statement.xml',
        'views/account_payment.xml',
        'views/account_move_line.xml',
		'views/voucher_type.xml',
        'views/account_journal.xml',
		'data/default_voucher_type.xml',
		'wizard/voucher_type_fixer.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}