from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json


class SPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    hr_department_id = fields.Many2one('hr.department', string='Department', required=True)
    check_send = fields.Boolean('Check Send', store=True)

    # Override check the creator has exceeded the limit
    def button_confirm(self):
        res_partner_user_id = self.env['res.partner'].search([('write_uid', '=', self.env.uid)])
        current_user_id = res_partner_user_id.mapped('id')
        employee_line = self.env['employee.order.limit'].search([], limit=1)
        employee = employee_line.mapped('order_limit')

        # get users of accountant
        id_group_accountant = self.env.cr.execute(
            "SELECT id FROM res_groups WHERE name::text LIKE '%Accountant%';")
        id_group_accountant_result = self.env.cr.fetchall()
        res_groups = self.env['res.groups'].sudo().search([('id', 'in', id_group_accountant_result)])
        res_groups_id = res_groups.mapped('users')
        res_groups_users = res_groups_id.mapped('id')

        # get partner_id of accountant
        res_users = self.env['res.users'].sudo().search([('id', 'in', res_groups_users)])
        res_users_id = res_users.mapped('partner_id')
        res_users_partner_id = res_users_id.mapped('id')

        # get id of accountant
        res_partner = self.env['res.partner'].sudo().search([('id', 'in', res_users_partner_id)])
        accountant_id = res_partner.mapped('id')

        for rec in self:
            if rec.amount_total:
                if (rec.amount_total < employee[0]) or (current_user_id[0] in accountant_id):
                    return super(SPurchaseOrder, self).button_confirm()
                else:
                    raise ValidationError('The total request exceeds the limit. Please send it to the accountant.')

    def btn_send(self):
        self.message_post(body=f'{self.create_uid.name} -> Confirmation request sent.')
        for rec in self:
            rec.check_send = True
