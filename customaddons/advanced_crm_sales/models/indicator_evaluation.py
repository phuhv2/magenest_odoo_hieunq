from odoo import models, fields, api


class IndicatorEvaluation(models.Model):
    _name = 'indicator.evaluation'

    sale_team_id = fields.Many2one('crm.team', string='Sale Team')
    real_revenue = fields.Float(string='Real Revenue', compute='_compute_real_revenue', store=False)
    month = fields.Char('Month', store=False, default=0)
    month_revenue = fields.Float('Month Revenue', compute='_compute_month_revenue', store=False)

    # Calculate real_revenue = amount_untaxed corresponding to the opportunity
    def _compute_real_revenue(self):
        for rec in self:
            if rec.sale_team_id:
                amount_untaxed_opportunity = self.env['sale.order'].search([('team_id', '=', rec.sale_team_id.mapped('id')), ('opportunity_id', '!=', False)])
                amount_untaxed = amount_untaxed_opportunity.mapped('amount_untaxed')
                rec.real_revenue = sum(amount_untaxed)

    # Get value month revenue to month of report
    def _compute_month_revenue(self):
        for rec in self:
            if rec.sale_team_id:
                month_sales_result = self.env['crm.team'].search([('id', '=', rec.sale_team_id.mapped('id'))])
                month_sales = month_sales_result.mapped(lambda res: (res.january_sales, res.february_sales, res.march_sales, res.april_sales, res.may_sales, res.june_sales, res.july_sales, res.august_sales, res.september_sales, res.october_sales, res.november_sales, res.december_sales))
                rec.month_revenue = month_sales[0][int(rec.month)]
