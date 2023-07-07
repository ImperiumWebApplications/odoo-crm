{
    'name': "Accounting Extension",
    'version': '1.0',
    'depends': ['base', 'web', 'account'],
    'author': "FonFon LLC",
    'description': """
    Extension for Accounting module
    """,
    'summary': 'Extension for Account module',
    'installable': True,
    'application': False,
    'license': 'Other proprietary',
    'data': [
        'views/account_ext_actions.xml',
        'views/account_ext_menu.xml',
    ],
}
