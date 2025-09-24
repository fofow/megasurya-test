{
    "name": "Megasurya Test Odoo Skill ",
    "summary": "Create New Module for Employee member and employee can update in portal",
    "version": "18.0.1.0.0",
    "author": "Faris Bassam",
    "license": "LGPL-3",
    "depends": ["hr", "portal"],
    "data": [
        "security/security_group.xml",
        "security/ir.model.access.csv",
        "views/employee_member_view.xml",
        "views/portal_templates.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "employee_family/static/src/scss/portal.scss",
        ],
    },
    "installable": True,
    "application": False
}