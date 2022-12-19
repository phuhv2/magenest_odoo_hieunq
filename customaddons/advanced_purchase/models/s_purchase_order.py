from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json


class SPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    hr_department_id = fields.Many2one('hr.department', string='Department', required=True)
    is_send = fields.Boolean('Is Send', store=True)

    # Override check the creator has exceeded the limit
    def button_confirm(self):
        current_uid = self.env.uid

        # get list id of accountant
        accountant_ids = self.env.ref('advanced_purchase.group_staff_accountant').users.ids

        # get order limit of current employee
        employee_line = self.env['employee.order.limit'].search([('employee_id', '=', current_uid)], limit=1)
        order_limit_employee = employee_line.mapped('order_limit')

        for rec in self:
            if rec.amount_total:
                if (rec.amount_total < order_limit_employee[0]) or (current_uid in accountant_ids):
                    return super(SPurchaseOrder, self).button_confirm()
                else:
                    raise ValidationError('The total request exceeds the limit. Please send it to the accountant.')

    def btn_send(self):
        self.message_post(body=f'{self.create_uid.name} -> Confirmation request sent.')
        for rec in self:
            rec.is_send = True
