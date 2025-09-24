import logging
from odoo import models,fields,api

_logger = logging.getLogger(__name__)

class EmployeeMember(models.Model):
    _name = "employee.family"

    name = fields.Char(string="Name", required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    family_relationship = fields.Selection([
        ("father", "Father"),
        ("mother", "Mother"),
        ("husband", "Husband"),
        ("wife", "Wife"),
        ("son", "Son"),
        ("daughter", "Daughter"),
        ("sibling", "Sibling")    
    ], string="Family Relationship", required=True)
    employee_id = fields.Many2one("hr.employee", string="Employee")
    notes = fields.Text(string="Notes")


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_family_ids = fields.One2many("employee.family", "employee_id", string="Employee Family")