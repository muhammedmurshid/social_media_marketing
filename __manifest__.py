{
    'name': "Social Media Marketing",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail'],
    'data': [
        'security/smm_groups.xml',
        'security/ir.model.access.csv',
        'data/activity.xml',
        'views/smm_records.xml',
        'views/smm_requirements.xml',
        'views/smm_agencies.xml',

    ],
    'demo': [],
    'images': [
        '/home/murshid/odoo/custome_addons/social_media_marketing/static/description/icon.png',
    ],
    'summary': "custom_addons_smm",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}
