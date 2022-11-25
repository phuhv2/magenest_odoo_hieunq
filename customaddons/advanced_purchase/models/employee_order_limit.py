from odoo import models, fields

class EmployeeOrderLimit(models.Model):
    _name = 'employee.order.limit'

    name = fields.Many2one('res.users', string='Employee Name')
    order_limit = fields.Float(string='Order Limit', digit=(12,3))
