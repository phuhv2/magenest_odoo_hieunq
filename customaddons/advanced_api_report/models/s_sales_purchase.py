from odoo import models, fields, api


class SSalesPurchase(models.Model):
    _name = 's.sales.purchase'

    def btn_send_email(self):
        # get list id of accountant
        accountant_ids = self.env.ref('advanced_purchase.group_staff_accountant').users.ids

        # get list partner_id of accountant
        res_users = self.env['res.users'].sudo().search([('id', 'in', accountant_ids)])
        res_users_id = res_users.mapped('partner_id')
        res_users_partner_id = res_users_id.mapped('id')

        # get list email of accountant
        res_partner = self.env['res.partner'].sudo().search([('id', 'in', res_users_partner_id)])
        email_accountant = res_partner.mapped('email')

        # get data indicator evaluation (crm_sales)
        indicator_evaluation = self.env['indicator.evaluation'].search([])
        sale_team = indicator_evaluation.mapped('sale_team_id')
        sale_team_name = sale_team.mapped('name')
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



    # Send mail for accountant
    # def btn_send_email(self):
    #     # get list id of accountant
    #     accountant_ids = self.env.ref('advanced_purchase.group_staff_accountant').users.ids
    #
    #     # get list partner_id of accountant
    #     res_users = self.env['res.users'].sudo().search([('id', 'in', accountant_ids)])
    #     res_users_id = res_users.mapped('partner_id')
    #     res_users_partner_id = res_users_id.mapped('id')
    #
    #     # get list email of accountant
    #     res_partner = self.env['res.partner'].sudo().search([('id', 'in', res_users_partner_id)])
    #     email_accountant = res_partner.mapped('email')
    #
    #     # get data indicator evaluation (crm_sales)
    #     indicator_evaluation = self.env['indicator.evaluation'].search([])
    #     sale_team = indicator_evaluation.mapped('sale_team_id')
    #     sale_team_name = sale_team.mapped('name')
    #     real_revenue = indicator_evaluation.mapped('real_revenue')
    #     real_revenue_difference = indicator_evaluation.mapped('real_revenue_difference')
    #
    #     # get data hr_department (purchase)
    #     hr_department = self.env['hr.department'].search([])
    #     department_name = hr_department.mapped('name')
    #     real_cost = hr_department.mapped('real_cost')
    #     real_cost_difference = hr_department.mapped('real_cost_difference')
    #
    #     template_obj = self.env['mail.template'].sudo().search([('model', 'like', 's.sales.purchase')], limit=1)
    #     if template_obj:
    #         sale_team_html = ""
    #         for name, revenue, diff in zip(sale_team_name, real_revenue, real_revenue_difference):
    #             sale_team_html += """
    #             <tr>
    #                 <td style="border: 1px solid black;">%s</td>
    #                 <td style="border: 1px solid black;">%s</td>
    #                 <td style="border: 1px solid black;">%s</td>
    #             </tr>
    #             """ % (name, revenue, diff)
    #
    #         department_html = ""
    #         for name, revenue, diff in zip(department_name, real_cost, real_cost_difference):
    #             department_html += """
    #             <tr>
    #                 <td style="border: 1px solid black;">%s</td>
    #                 <td style="border: 1px solid black;">%s</td>
    #                 <td style="border: 1px solid black;">%s</td>
    #             </tr>
    #             """ % (name, revenue, diff)
    #
    #         body = """
    #         <h3 style="color: red;">I. Kinh doanh</h3>
    #         <table style="border: 1px solid black; border-collapse: collapse; width:900px;">
    #             <tr>
    #                 <th style="border: 1px solid black; width:300px;">Tên nhóm bán hàng</th>
    #                 <th style="border: 1px solid black; width:300px;">Doanh thu thực tế</th>
    #                 <th style="border: 1px solid black; width:300px;">Chênh lệch doanh thu thực tế so với chỉ tiêu tháng hiện tại</th>
    #             </tr>
    #             %s
    #         </table>
    #         <h3 style="color: red;">II. Mua hàng</h3>
    #         <table style="border: 1px solid black; border-collapse: collapse; width:900px;">
    #             <tr>
    #                 <th style="border: 1px solid black; width:300px;">Tên phòng ban</th>
    #                 <th style="border: 1px solid black; width:300px;">Chi tiêu thực tế</th>
    #                 <th style="border: 1px solid black; width:300px;">Chênh lệch chi tiêu thực tế so với hạn mức</th>
    #             </tr>
    #             %s
    #         </table>
    #         """ % (sale_team_html, department_html)
    #
    #         receipt_list = email_accountant
    #         mail_values = {
    #             'subject': template_obj.subject,
    #             'body_html': body,
    #             'email_to': ';'.join(map(lambda x: x, receipt_list)),
    #             'email_from': 'laravel.ecommerce.v1@gmail.com',
    #         }
    #         self.env['mail.mail'].create(mail_values).send()
