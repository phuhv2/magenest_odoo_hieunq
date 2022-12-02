from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SCrmLead(models.Model):
    _inherit = 'crm.lead'

    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
    minimum_revenue = fields.Float('Minium Revenue (VAT)')
    check_edit = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Check Edit', default='yes')
    real_revenue = fields.Float(string='Real Revenue', compute='_compute_real_revenue', store=True)
    create_month = fields.Integer('Create Month', compute='_compute_create_month', store=False)

    @api.constrains('minimum_revenue')
    def _check_minimum_revenue(self):
        if self.minimum_revenue:
            if self.minimum_revenue < 0:
                raise ValidationError("The expected price must be strictly positive")

    @api.onchange('check_edit')
    def _onchange_check_edit(self):
        if self.check_edit:
            count_sale_order = self.env['sale.order'].search_count([('opportunity_id', '=', self.id)])
            if count_sale_order > 0:
                self.check_edit = 'no'

    # Get data into view tree of real_revenue
    @api.depends('name')
    def _compute_real_revenue(self):
        for rec in self:
            if rec.name:
                amount_total = self.env['sale.order'].search([('opportunity_id', '=', rec.name)])
                amount_total_opportunity = amount_total.mapped('amount_total')
                rec.real_revenue = sum(amount_total_opportunity)
            else:
                rec.real_revenue = 0

    # Get create_month of create_date
    @api.depends('create_date')
    def _compute_create_month(self):
        for rec in self:
            if rec.create_date:
                create_date = str(rec.create_date)
                create_month = create_date.split("-")
                rec.create_month = create_month[1]
