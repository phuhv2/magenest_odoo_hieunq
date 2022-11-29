from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SHrDepartment(models.Model):
    _inherit = 'hr.department'

    spending_limit = fields.Float('Spending Limit/Month', digits=(12,3))
    real_revenue = fields.Float('Real Revenue', digits=(12,3), compute='_compute_real_revenue', store=True)

    @api.constrains('spending_limit')
    def _check_spending_limit(self):
        for rec in self:
            if rec.spending_limit<0:
                raise ValidationError("The expected price must be strictly positive")


    @api.depends('name')
    def _compute_real_revenue(self):
        for rec in self:
            self.env.cr.execute("""
                SELECT SUM(purchase_order.amount_total)
                FROM hr_department 
                INNER JOIN purchase_order
                ON hr_department.id=purchase_order.hr_department_id
                WHERE hr_department.name LIKE '%s'
                GROUP BY hr_department.name
            """% (rec.name))
            results = self.env.cr.fetchall()
            rec.real_revenue = results[0][0]