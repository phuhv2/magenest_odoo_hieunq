from odoo import models, fields, api


class SsHrDepartment(models.Model):
    _inherit = 'hr.department'

    real_cost_difference = fields.Float('Real Cost Difference', compute='_compute_real_cost_difference')

    def _compute_real_cost_difference(self):
        for rec in self:
            rec.real_cost_difference = 0
            if rec.spending_limit:
                rec.real_cost_difference = rec.real_cost - rec.spending_limit
