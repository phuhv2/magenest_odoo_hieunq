from odoo import models, fields, api


class IndicatorEvaluation(models.Model):
    _name = 'indicator.evaluation'

    sale_order_id = fields.Many2one('crm.lead', string='Sale Order')
    sale_team = fields.Many2one(related='sale_order_id.sales_team_id', string='Sale Team')
    real_revenue = fields.Float(string='Real Revenue', compute='_compute_real_revenue', store=True)
    month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', default='1')
    monthly_sales = fields.Float('Revenue Targets', compute='_compute_monthly_sales')
    create_month = fields.Integer('Create Month', compute='_compute_create_month', store=False)

    @api.depends('sale_order_id')
    def _compute_real_revenue(self):
        for rec in self:
            if rec.sale_order_id:
                sale_order = rec.sale_order_id.mapped('id')
                for id in sale_order:
                    amount_untaxed = self.env['sale.order'].search([('opportunity_id', '=', id)])
                    amount_untaxed_opportunity = amount_untaxed.mapped('amount_untaxed')
                    rec.real_revenue = sum(amount_untaxed_opportunity)

    @api.onchange('sale_team', 'month')
    def _compute_monthly_sales(self):
        results = self.env['crm.team'].search([('id', '=', self.sale_team.id)])
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

    # Get create_month of create_date
    @api.depends('create_date')
    def _compute_create_month(self):
        for rec in self:
            if rec.create_date:
                create_date = str(rec.create_date)
                create_month = create_date.split("-")
                rec.create_month = create_month[1]
