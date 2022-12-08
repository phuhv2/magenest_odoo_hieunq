from odoo import models, fields, api
from datetime import date

class SalesPurchase(models.Model):
    _name = 'sales.purchase'

    sale_team_id = fields.Many2one('crm.team', string='Sale Team')
    real_revenue = fields.Float('Real Revenue', compute='_compute_real_revenue', store=False)
    difference_between_revenue = fields.Float('The difference between revenue', compute='_compute_difference_between_revenue', store=True)
    department_id = fields.Many2one('hr.department', string='Department')
    real_revenue_department = fields.Float('Real Revenue Department', compute='_compute_real_revenue_department')
    spending_limit = fields.Float('Spending Limit/Month', related='department_id.spending_limit')
    difference_between_spending = fields.Float('The difference between revenue', compute='_compute_difference_between_spending', store=True)

    def _compute_real_revenue(self):
        for rec in self:
            if rec.sale_team_id:
                indicator_evaluation = self.env['indicator.evaluation'].search([('sale_team_id', 'in', rec.sale_team_id.mapped('id')),
                                                                                ('month', '=', int(date.today().month))], limit=1)
                real_revenue = indicator_evaluation.mapped('real_revenue')
                rec.real_revenue = real_revenue[0]

    @api.depends('real_revenue')
    def _compute_difference_between_revenue(self):
        for rec in self:
            indicator_evaluation = self.env['indicator.evaluation'].search(
                [('sale_team_id', 'in', rec.sale_team_id.mapped('id')),
                 ('month', '=', int(date.today().month))], limit=1)
            month_revenue = indicator_evaluation.mapped('month_revenue')
            if rec.real_revenue:
                rec.difference_between_revenue = rec.real_revenue - month_revenue[0]


    def _compute_real_revenue_department(self):
        for rec in self:
            if rec.department_id:
                hr_department = self.env['hr.department'].search([('id', 'in', rec.department_id.mapped('id'))])
                real_revenue_department = hr_department.mapped('real_revenue')
                rec.real_revenue_department = real_revenue_department[0]

    @api.depends('real_revenue_department', 'spending_limit')
    def _compute_difference_between_spending(self):
        for rec in self:
            if rec.real_revenue_department and rec.spending_limit:
                rec.difference_between_spending = rec.real_revenue_department - rec.spending_limit

    # @api.model
    # def update_records(self):
    #     sales_purchase = self.env['sales.purchase'].search([])
    #
    #     records = self.env['sales.purchase'].search([])
    #     for record in records:
    #         record.write({
    #             'sale_team_id': id,
    #         })