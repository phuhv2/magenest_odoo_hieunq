from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class IndicatorEvaluation(models.Model):
    _name = 'indicator.evaluation'
    _description = 'Indicator Evaluation'

    sales_team_ids = fields.Many2one('crm.team', string='Sales Team')
    real_revenue = fields.Float('Real Revenue', digits=(12, 3), compute='_compute_real_revenue', store=True)
    month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', default='1')
    monthly_sales = fields.Float('Revenue Targets', compute='_compute_monthly_sales', digits=(12, 3))
    opportunity_ids = fields.Many2one('crm.lead', string='Opportunity')

    @api.onchange('sales_team_ids', 'month')
    def _compute_monthly_sales(self):
        results = self.env['crm.team'].search([('id', '=', self.sales_team_ids.id)])
        for rec in self:
            if rec.month == '1':
                rec.monthly_sales = results.january_sales
            elif rec.month == '2':
                rec.monthly_sales = results.february_sales
            elif rec.month == '3':
                rec.monthly_sales = results.march_sales
            elif rec.month == '4':
                rec.monthly_sales = results.april_sales
            elif rec.month == '5':
                rec.monthly_sales = results.may_sales
            elif rec.month == '6':
                rec.monthly_sales = results.june_sales
            elif rec.month == '7':
                rec.monthly_sales = results.july_sales
            elif rec.month == '8':
                rec.monthly_sales = results.august_sales
            elif rec.month == '9':
                rec.monthly_sales = results.september_sales
            elif rec.month == '10':
                rec.monthly_sales = results.october_sales
            elif rec.month == '11':
                rec.monthly_sales = results.november_sales
            else:
                rec.monthly_sales = results.december_sales

    @api.depends('opportunity_ids')
    def _compute_real_revenue(self):
        for rec in self:
            self.env.cr.execute("""
                SELECT SUM(sale_order.amount_untaxed), crm_lead.name 
                FROM sale_order 
                INNER JOIN crm_lead 
                ON sale_order.team_id=crm_lead.team_id 
                INNER JOIN indicator_evaluation 
                ON indicator_evaluation.opportunity_ids=crm_lead.id 
                WHERE indicator_evaluation.opportunity_ids=%s
                GROUP BY crm_lead.name
            """ % (rec.opportunity_ids.id))
            results = self.env.cr.fetchall()
            rec.real_revenue = results[0][0]

