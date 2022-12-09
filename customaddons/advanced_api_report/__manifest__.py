# -*- coding: utf-8 -*-
{
    'name': "API Report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'advanced_crm_sales', 'advanced_purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/s_sales_purchase_cron.xml',
        'data/s_sales_purchase_email_template.xml',
        'views/s_sales_purchase.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
