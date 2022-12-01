from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SHrDepartment(models.Model):
    _inherit = 'hr.department'

    spending_limit = fields.Float('Spending Limit/Month', digits=(12,3))
    real_revenue = fields.Float('Real Revenue', digits=(12,3), compute='_compute_real_revenue', store=True)
    create_month = fields.Integer('Create Month', compute='_compute_create_month', store=False)

    @api.constrains('spending_limit')
    def _check_spending_limit(self):
        for rec in self:
            if rec.spending_limit<0:
                raise ValidationError("The expected price must be strictly positive")

    # Get data into view tree of real_revenue
    @api.depends('name')
    def _compute_real_revenue(self):
        for rec in self:
            self.env.cr.execute("""
                SELECT SUM(purchase_order.amount_total) AS real_revenue
                FROM hr_department 
                INNER JOIN purchase_order
                ON hr_department.id=purchase_order.hr_department_id
                WHERE hr_department.name LIKE '%s'
                GROUP BY hr_department.name
            """% (rec.name))
            results = self.env.cr.dictfetchall()
            rec.real_revenue = results[0]['real_revenue']

    # Get create_month of create_date
    @api.depends('create_date')
    def _compute_create_month(self):
        for rec in self:
            if rec.create_date:
                create_date = str(rec.create_date)
                create_month = create_date.split("-")
                rec.create_month = create_month[1]