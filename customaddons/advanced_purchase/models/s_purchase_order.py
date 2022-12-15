from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    hr_department_id = fields.Many2one('hr.department', string='Department', required=True)
    check_send = fields.Boolean('Check Send', store=True)

    # Override check the creator has exceeded the limit
    def button_confirm(self):
        current_user_id = self.env.uid
        employee_line = self.env['employee.order.limit'].search([('name', '=', current_user_id)], limit=1)
        employee = employee_line.mapped('order_limit')

        # get users of accountant
        res_groups = self.env['res.groups'].sudo().search([('id', '=', 52)])
        res_groups_id = res_groups.mapped('users')
        res_groups_users = res_groups_id.mapped('id')

        # get partner_id of accountant
        res_users = self.env['res.users'].sudo().search([('id', 'in', res_groups_users)])
        res_users_id = res_users.mapped('partner_id')
        res_users_partner_id = res_users_id.mapped('id')

        # get email of accountant
        res_partner = self.env['res.partner'].sudo().search([('id', 'in', res_users_partner_id)])
        accountant_id = res_partner.mapped('id')

        for rec in self:
            if rec.amount_total:
                if current_user_id in accountant_id:
                    return super(SPurchaseOrder, self).button_confirm()
                elif rec.amount_total < employee[0] and rec.check_send == False:
                    return super(SPurchaseOrder, self).button_confirm()
                else:
                    raise ValidationError('The total request exceeds the limit. Please send it to the accountant.')

    def btn_send(self):
        self.message_post(body=f'{self.create_uid.name} -> Confirmation request sent.')
        for rec in self:
            rec.check_send = True

    # Override button confirm for accountant
    # def btn_confirm_order(self):
    #     return super(SPurchaseOrder, self).button_confirm()
