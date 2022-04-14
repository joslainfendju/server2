# -*- coding: utf-8 -*-
{
    'name': "nh_3n_pharma_requirement_setup_ce",

    'summary': """
        This module purpose is to deploy all modules 
        that are required for t 3N PHARMA specification book V1.0.
        """,

    'description': """
        This module purpose is to deploy all modules 
        that are required for t 3N PHARMA specification book V1.0.
    """,
    'application': True,
    'author': "ITS",
    'website': "http://www.its-nh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'All',
    'version': '0.1',

    #python libs required
    'external_dependencies': {
        'python': ['jdcal', 'openpyxl'],
    },
    # any module necessary for this one to work correctly
    'depends': [
        'nh_3n_pharma_sale_process_credit_limit',
        'auth_session_timeout',
        'nh_3n_constraint_sn_available_qty',
        'nh_3n_internal_transfert',
        'nh_product_dict',
        'nh_product_move_report',
        'nh_refresh_uom',
        'nh_scm_stock_transit_report',
        'nh_scm_stock_wise_report',
        'nh_transit_periodic_alert',
        'nh_control_order_return_infos',
        'nh_3n_pharma_stock_ajustment_wkf',
        'nh_3n_pharma_expiry_periodic_alert',
        'nh_3n_pharma_customer_supplier_infos',
        'nh_3n_pharma_payement_alert',
        'nh_sale_commission_v11',
        'nh_sale_price_control',
        'nh_credit_limit_report_ce',
        'nh_3n_pharma_sale_promotion_buyX_getY',
        'nh_3n_report_update',
        'nh_budget_managment_CE',
        'nh_voucher_from_cash_and_bank_CE',
        'nh_dash_board',
        'nh_direct_invoice_from_delivery_order_v11',
        'nh_expiration_date_on_delivery_order',
        'nh_expiry_report',
        'nh_high_sea_report',
        'nh_invoice__qr',
        'nh_tko_web_sessions_management',
        'nh_3n_initial_balance_import',
        'nh_account_chart_import',
        'nh_3n_initial_stock_correct',
        'nh_3n_inventory_back_date'
    ],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/yangon_import_setting.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}