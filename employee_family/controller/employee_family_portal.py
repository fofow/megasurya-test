from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import logging

_logger = logging.getLogger(__name__)

class EmployeeFamilyPortal(CustomerPortal):
    
    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        for employee in request.env.user.partner_id.employee_ids:
            _logger.info("Employee: %s", employee)
            employee = employee.id
            values['has_family_access'] = bool(employee)
        return values

    #List  Family
    @http.route(['/my/family', '/my/family/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_family(self, **kwargs):
        for employee in request.env.user.partner_id.employee_ids:
            _logger.info("Employee: %s", employee)
            employee = employee.id

        # employee = request.env['hr.employee'].sudo().search([
        #     ('user_id', '=', request.env.user.id)
        # ], limit=1)
            if not employee:
                return request.redirect('/my')
                
            family_members = request.env['employee.family'].sudo().search([('employee_id', '=', employee)])
            
            values = {
                'page_name': 'family',
                'family_members': family_members,
                'employee': employee,
            }
            return request.render("employee_family.portal_my_family_page", values)

    #Create Family Member
    @http.route(['/my/family/new'], type='http', auth="user", website=True)
    def create_family_member(self, **kwargs):
        for employee in request.env.user.partner_id.employee_ids:
            employee = employee.id
            if not employee:
                return request.redirect('/my')
                
            if request.httprequest.method == 'POST':
                vals = {
                    'name': request.params.get('name'),
                    'family_relationship': request.params.get('family_relationship'),
                    'date_of_birth': request.params.get('date_of_birth'),
                    'employee_id': employee,
                    'notes': request.params.get('notes', ''),
                }
                request.env['employee.family'].sudo().create(vals)
                return request.redirect('/my/family')
                
            values = {
                'page_name': 'family',
                'employee': employee,
            }
            return request.render("employee_family.portal_family_form", values)

    #Edit Family Member
    @http.route(['/my/family/<int:family_id>/edit'], type='http', auth="user", website=True)
    def edit_family_member(self, family_id, **kwargs):
        for employee in request.env.user.partner_id.employee_ids:
            employee = employee.id
            family = request.env['employee.family'].sudo().browse(family_id)
            _logger.info("Employee: %s", employee)
            _logger.info("Family: %s", family)            
            if not employee or not family.exists() or family.employee_id.id != employee:
                return request.redirect('/my/family')
                
            if request.httprequest.method == 'POST':
                family.sudo().write({
                    'name': request.params.get('name'),
                    'family_relationship': request.params.get('family_relationship'),
                    'date_of_birth': request.params.get('date_of_birth'),
                    'notes': request.params.get('notes', ''),
                })
                return request.redirect('/my/family')
                
            values = {
                'page_name': 'family',
                'record': family,
                'employee': employee,
            }
            return request.render("employee_family.portal_family_form", values)

    #Delete Family Member
    @http.route(['/my/family/<int:family_id>/delete'], type='http', auth="user", website=True)
    def delete_family_member(self, family_id, **kwargs):
        for employee in request.env.user.partner_id.employee_ids:
            employee = employee.id
            family = request.env['employee.family'].sudo().browse(family_id)
            
            if not employee or not family.exists() or family.employee_id.id != employee:
                return request.redirect('/my/family')
                
            if employee and family.exists() and family.employee_id.id == employee:
                family.sudo().unlink()
            
        return request.redirect('/my/family')