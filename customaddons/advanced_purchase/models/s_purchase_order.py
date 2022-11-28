from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    hr_department_id = fields.Many2one('hr.department', string='Department', required=True)
    check_confirm = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Check Confirm')

    #Override
    def button_confirm(self):
        for res in self:
            employee_line = self.env['employee.order.limit'].search([('name', '=', res.create_uid.id)], limit=1)
            employee = employee_line.mapped('order_limit')
            for rec in self:
                if rec.amount_total < employee[0]:
                    result = super(SPurchaseOrder, self).button_confirm()
                    return result
                else:
                    rec.check_confirm = 'no'
                    raise ValidationError('You do not have the right to confirm your request for a quote.')

    def btn_send(self):
        noti_send = f'({self.create_uid.name}) {fields.Datetime.now()} -> Confirmation request sent.'
        self.message_post(subject='Send to accountant', body=noti_send, message_type='notification')
        for rec in self:
            rec.check_confirm = 'yes'
