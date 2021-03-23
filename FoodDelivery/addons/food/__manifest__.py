{
    'name': 'Food Delivery',
    'version': '1.0',
    'category': 'Food Delivery',
    'sequence': 5,
    'summary': 'Food delivery system',
    'description': "",
    'website': '',
    'depends': ['mail', 'web', 'website', 'board', 'report_xlsx'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'wizard/payment_wizard_view.xml',

#       'views/customers_view.xml',
        'views/report/ordered_report.xml',
        'views/report/my_report_template.xml',
        'views/res_partner_view.xml',
        'views/category_view.xml',
        'views/products_view.xml',
        'views/orders_view.xml',
        'views/payment_view.xml',
        
        'views/menu.xml',
        'views/dash.xml',
        'views/client_actions_view.xml',

        'wizard/product_update_wizard_view.xml',
        'wizard/date_wizard_view.xml',

        'data/sequence.xml',
        'data/template.xml',
        'data/category_data.xml',
#         'data/email_cron.xml',
        'data/email_template.xml',
#         'data/good_morning_email.xml',
        'data/sample_server_action_data.xml',
        'data/website_menu.xml',
    ],
    'demo': [
    ],
    'qweb': [
        "static/src/xml/*.xml"
    ],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False
    
#      --test-enable -d yesu-food -i food --stop-after-init
}