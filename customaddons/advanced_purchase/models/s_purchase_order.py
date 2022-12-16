from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json


class SPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    hr_department_id = fields.Many2one('hr.department', string='Department', required=True)
    check_send = fields.Boolean('Check Send', store=True)

    # Override check the creator has exceeded the limit
    def button_confirm(self):
        current_uid = self.env.uid

        # get list id of accountant
        id_group_accountant = self.env.cr.execute(
            "SELECT id FROM res_groups WHERE name::text LIKE '%Accountant%';")
        id_group_accountant_result = self.env.cr.fetchall()
        res_groups = self.env['res.groups'].sudo().search([('id', 'in', id_group_accountant_result)])
        res_groups_id = res_groups.mapped('users')
        res_groups_users = res_groups_id.mapped('id')

        # get order limit of current employee
        employee_line = self.env['employee.order.limit'].search([], limit=1)
        employee = employee_line.mapped('order_limit')

        for rec in self:
            if rec.amount_total:
                if (rec.amount_total < employee[0]) or (current_uid in res_groups_users):
                    return super(SPurchaseOrder, self).button_confirm()
                else:
                    raise ValidationError('The total request exceeds the limit. Please send it to the accountant.')

    def btn_send(self):
        self.message_post(body=f'{self.create_uid.name} -> Confirmation request sent.')
        for rec in self:
            rec.check_send = True
