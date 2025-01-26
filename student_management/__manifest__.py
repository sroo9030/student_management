# -*- coding: utf-8 -*-
{
    'name': "student_management",

    'summary': """
        Basic Odoo Module Creation
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Eisra",
    'email': "eng.eisraosama@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'common', 'mail', 'contacts', 'documents'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/views.xml',
        'views/teacher.xml',
        'views/course.xml',
        'views/staff.xml',
        'views/student_class.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
