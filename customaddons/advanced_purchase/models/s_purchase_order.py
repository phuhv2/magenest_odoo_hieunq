from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    hr_department_id = fields.Many2one('hr.department', string='Department', required=True)

    # Override check the creator has exceeded the limit
    def button_confirm(self):
        current_user_id = self.env.uid
        employee_line = self.env['employee.order.limit'].search([('name', '=', current_user_id)], limit=1)
        employee = employee_line.mapped('order_limit')
        for rec in self:
            if rec.amount_total:
                if rec.amount_total < employee[0]:
                    return super(SPurchaseOrder, self).button_confirm()
                else:
                    raise ValidationError('The total request exceeds the limit. Please send it to the accountant.')

    def btn_send(self):
        self.message_post(body=f'{self.create_uid.name} -> Confirmation request sent.')

    # Override button confirm for accountant
    def btn_confirm_order(self):
        return super(SPurchaseOrder, self).button_confirm()
