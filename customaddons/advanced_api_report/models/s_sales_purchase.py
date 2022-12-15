from odoo import models, fields, api

class SSalesPurchase(models.Model):
    _name = 's.sales.purchase'


    # Send mail for accountant
    def btn_send_email(self):
        #get users of accountant
        res_groups = self.env['res.groups'].sudo().search([('id', '=', 52)])
        res_groups_id = res_groups.mapped('users')
        res_groups_users = res_groups_id.mapped('id')

        #get partner_id of accountant
        res_users = self.env['res.users'].sudo().search([('id', 'in', res_groups_users)])
        res_users_id = res_users.mapped('partner_id')
        res_users_partner_id = res_users_id.mapped('id')


        #get email of accountant
        res_partner = self.env['res.partner'].sudo().search([('id', 'in', res_users_partner_id)])
        email_accountant = res_partner.mapped('email')

        # get data sales (indicator evaluation)
        indicator_evaluation = self.env['indicator.evaluation'].search([])
        sale_team = indicator_evaluation.mapped('sale_team_id')
        sale_teams = sale_team.mapped('name')
        real_revenue = indicator_evaluation.mapped('real_revenue')
        revenue_difference = indicator_evaluation.mapped('revenue_difference')

        #get data hr_department
        hr_department = self.env['hr.department'].search([])
        department_name = hr_department.mapped('name')
        department_real_revenue = hr_department.mapped('real_revenue')
        department_revenue_difference = hr_department.mapped('revenue_difference')


        template_obj = self.env['mail.template'].sudo().search([('model', 'like', 's.sales.purchase')], limit=1)
        if template_obj:
            sale_team_html = ""
            for name, revenue, diff in zip(sale_teams, real_revenue, revenue_difference):
                sale_team_html += """
                <tr>
                    <td style="border: 1px solid black;">%s</td>
                    <td style="border: 1px solid black;">%s</td>
                    <td style="border: 1px solid black;">%s</td>
                </tr>
                """% (name, revenue, diff)

            department_html = ""
            for name, revenue, diff in zip(department_name, department_real_revenue, department_revenue_difference):
                department_html += """
                <tr>
                    <td style="border: 1px solid black;">%s</td>
                    <td style="border: 1px solid black;">%s</td>
                    <td style="border: 1px solid black;">%s</td>
                </tr>
                """% (name, revenue, diff)


            body = """
            <h3 style="color: red;">I. Kinh doanh</h3>
            <table style="border: 1px solid black; border-collapse: collapse; width:900px;">
                <tr>
                    <th style="border: 1px solid black; width:300px;">Tên nhóm bán hàng</th>
                    <th style="border: 1px solid black; width:300px;">Doanh thu thực tế</th>
                    <th style="border: 1px solid black; width:300px;">Chênh lệch doanh thu thực tế so với chỉ tiêu tháng hiện tại</th>
                </tr>
                %s
            </table>
            <h3 style="color: red;">II. Mua hàng</h3>
            <table style="border: 1px solid black; border-collapse: collapse; width:900px;">
                <tr>
                    <th style="border: 1px solid black; width:300px;">Tên phòng ban</th>
                    <th style="border: 1px solid black; width:300px;">Chi tiêu thực tế</th>
                    <th style="border: 1px solid black; width:300px;">Chênh lệch chi tiêu thực tế so với hạn mức</th>
                </tr>
                %s
            </table>
            """% (sale_team_html, department_html)

            receipt_list = email_accountant
            mail_values = {
                'subject': template_obj.subject,
                'body_html': body,
                'email_to': ';'.join(map(lambda x: x, receipt_list)),
                'email_from': 'laravel.ecommerce.v1@gmail.com',
            }
            self.env['mail.mail'].create(mail_values).send()


