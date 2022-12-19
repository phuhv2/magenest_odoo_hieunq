from odoo import models, fields, api


class SsHrDepartment(models.Model):
    _inherit = 'hr.department'

    real_cost_difference = fields.Float('Real Cost Difference', compute='_compute_real_cost_difference', store=True)

    def _compute_real_cost_difference(self):
        for rec in self:
            if rec.real_cost:
                rec.real_cost_difference = rec.real_cost - rec.spending_limit
