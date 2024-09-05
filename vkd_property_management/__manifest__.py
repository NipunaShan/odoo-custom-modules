# -*- coding: utf-8 -*-

{
    'name': "Property Management",
    'version': '17.0.1.0.0',
    'category': '',
    'summary': """ """,
    'description': """ """,

    'author': "VK Data ApS",
    'website': "https://vkdata.dk",

    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/unit_reservation_sequence_data.xml',
        'data/ir_cron_data.xml',
        'views/property_management_menus.xml',
        'views/apartment_details_views.xml',
        'views/floor_details_views.xml',
        'views/unit_details_views.xml',
        'views/sale_agent_views.xml',
        'views/res_config_settings_views.xml',
        'views/unit_reservation_views.xml',
        'views/tower_details_views.xml',
        'views/sale_agent_categories_views.xml',
    ],
    'license': 'OPL-1',
    'application': True,
    'installable': True,
    'auto_install': False,

}
