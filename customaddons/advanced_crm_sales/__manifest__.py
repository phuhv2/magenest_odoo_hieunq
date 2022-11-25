# -*- coding: utf-8 -*-
{
    'name': "Advanced CRM Sales",

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
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/plan_sale_order_views.xml',
        'views/sale_order_views.xml',
        'views/sale_team_views.xml',
        'views/crm_lead_views.xml',
        'wizard/detail_report_wizard_views.xml',
        'views/crm_lead_tree_views.xml',
        'wizard/indicator_evaluation_report_wizard_views.xml',
        'views/indicator_evaluation_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
