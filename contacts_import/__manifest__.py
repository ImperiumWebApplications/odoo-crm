{
    'name': "ContactsImport",
    'summary': "Import Contacts from CSV",
    'description': "This module imports contacts from a CSV file.",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'contacts'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/import_wizard_view.xml',
        'views/import_wizard_menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
