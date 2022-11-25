from odoo import models, fields, api
from datetime import datetime

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _sql_constraints = [
        ("check_minimum_revenue", "CHECK(minimum_revenue > 0)", "The expected price must be strictly positive")
    ]

    minimum_revenue = fields.Float('Minium Revenue (VAT)', digits=(12, 3))
    sales_team = fields.Many2one('crm.team', string='Sales Team')
    create_month = fields.Char('Create Month', compute='_compute_create_month', readonly=True)
    real_revenue = fields.Float(string="Real Revenue", compute='_compute_real_revenue')

    @api.depends('create_date')
    def _compute_create_month(self):
        for rec in self:
            rec.create_month = rec.create_date.split('-')[1]

    @api.depends('name')
    def _compute_real_revenue(self):
        for rec in self:
            self.env.cr.execute("""
                SELECT SUM(sale_order.amount_total), crm_lead.name
                FROM sale_order
                INNER JOIN crm_lead
                ON sale_order.team_id=crm_lead.team_id
                WHERE crm_lead.name='%s'
                GROUP BY crm_lead.name
            """%(rec.name))
            results = self.env.cr.fetchall()
            rec.real_revenue = results[0][0]













