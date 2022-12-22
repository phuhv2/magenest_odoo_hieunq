from odoo import models, fields, api


class SSalesPurchase(models.Model):
    _name = 's.sales.purchase'

    def btn_send_email(self):
        # get list id of accountant
        accountant_ids = self.env.ref('advanced_purchase.group_staff_accountant').users.ids

        # get list partner_id of accountant
        res_users = self.env['res.users'].sudo().search([('id', 'in', accountant_ids)])
        res_users_partner_id = res_users.mapped('partner_id.id')

        # get list email of accountant
        res_partner = self.env['res.partner'].sudo().search([('id', 'in', res_users_partner_id)])
        email_accountant = res_partner.mapped('email')

        # get data indicator evaluation (crm_sales)
        indicator_evaluation = self.env['indicator.evaluation'].search([])
        sale_team_name = indicator_evaluation.mapped('sale_team_id.name')
        real_revenue = indicator_evaluation.mapped('real_revenue')
        real_revenue_difference = indicator_evaluation.mapped('real_revenue_difference')

        # get data hr_department (purchase)
        hr_department = self.env['hr.department'].search([])
        department_name = hr_department.mapped('name')
        real_cost = hr_department.mapped('real_cost')
        real_cost_difference = hr_department.mapped('real_cost_difference')

        ctx = {}
        ctx['sale_team_name'] = sale_team_name
        ctx['real_revenue'] = real_revenue
        ctx['real_revenue_difference'] = real_revenue_difference
        ctx['department_name'] = department_name
        ctx['real_cost'] = real_cost
        ctx['real_cost_difference'] = real_cost_difference
        ctx['email_to'] = ';'.join(map(lambda x: x, email_accountant))
        ctx['email_from'] = 'laravel.ecommerce.v1@gmail.com'
        template = self.env.ref('advanced_api_report.email_template')
        template.with_context(ctx).send_mail(self.id, force_send=True, raise_exception=False)
