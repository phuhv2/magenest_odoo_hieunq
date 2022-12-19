from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EmployeeOrderLimit(models.Model):
    _name = 'employee.order.limit'

    employee_id = fields.Many2one('res.users', string='Employee Name')
    order_limit = fields.Float(string='Order Limit', digit=(12, 3))

    @api.constrains('order_limit')
    def _check_order_limit(self):
        if self.order_limit:
            if self.order_limit < 0:
                raise ValidationError('The expected price must be strictly positive')
