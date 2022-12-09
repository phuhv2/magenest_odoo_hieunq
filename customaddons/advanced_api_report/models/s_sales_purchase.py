from odoo import models, fields, api

class SSalesPurchase(models.Model):
    _name = 's.sales.purchase'

    @api.model
    def update_records(self):
        pass

    # Send mail for account
    def btn_send_email(self):
        #lay users cua ba ke toan
        res_groups = self.env['res.groups'].sudo().search([('id', '=', 52)])
        res_groups_id = res_groups.mapped('users')
        res_groups_users = res_groups_id.mapped('id')  # [2]

        #
        res_users = self.env['res.users'].sudo().search([('id', 'in', res_groups_users)])
        res_users_id = res_users.mapped('partner_id')
        res_users_partner_id = res_users_id.mapped('id')


        #
        res_partner = self.env['res.partner'].sudo().search([('id', 'in', res_users_partner_id)])
        email_accountant = res_partner.mapped('email')

        template_obj = self.env['mail.template'].sudo().search([('model', 'like', 's.sales.purchase')], limit=1)
        if template_obj:
            receipt_list = email_accountant
            body = template_obj.body_html

            mail_values = {
                'subject': template_obj.subject,
                'body_html': body,
                'email_to': ';'.join(map(lambda x: x, receipt_list)),
                'email_from': 'laravel.ecommerce.v1@gmail.com',
            }
            self.env['mail.mail'].create(mail_values).send()
