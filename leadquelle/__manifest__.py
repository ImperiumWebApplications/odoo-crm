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
    ],
    'route': [
        '/api/v1', 'leadquelle.controllers.API:APIEndpoint',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'icon': 'static/description/icon.png',
}
