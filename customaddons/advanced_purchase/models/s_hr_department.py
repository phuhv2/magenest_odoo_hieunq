from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SHrDepartment(models.Model):
    _inherit = 'hr.department'

    spending_limit = fields.Float('Spending Limit/Month', digits=(12,3))

    @api.constrains('spending_limit')
    def _check_spending_limit(self):
        for rec in self:
            if rec.spending_limit<0:
                raise ValidationError("The expected price must be strictly positive")

