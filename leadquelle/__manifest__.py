{
    'name': "Leadquelle",
    'version': '1.0',
    'depends': ['base', 'web', 'account'],
    'author': "Leadquelle GmbH",
    'description': """
    Lead management app for Odoo Platform
    """,
    'summary': 'Lead management app for Odoo Platform',
    'installable': True,
    'application': True,
    'license': 'Other proprietary',
    'data': [
        'data/ir.model.access.csv',
        'data/manager_views.xml',
        'data/integration_views.xml',
        'data/leadquelle_menus.xml',
        'data/leadquelle.manager.model.csv',
        'views/res_partner_view.xml',
    ],
    'route': [
        '/api/v1', 'leadquelle.controllers.API:APIEndpoint',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'icon': 'static/description/icon.png',
}
