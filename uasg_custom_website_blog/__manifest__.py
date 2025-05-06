# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'UASG Custom Website Blog',
    'category': 'Tools',
    'description': """
The module Add a features to odoo Blog
===========================================
""",
    'author' : 'Amal Abdelmajid / UASG',
    'depends': ['base','website_blog'],
    'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'views/views.xml',
    'views/documentsview.xml',
    'views/documents_portal.xml'
       
    ],
    'license': 'LGPL-3',
}
