from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SCrmLead(models.Model):
    _inherit = 'crm.lead'

    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
    minimum_revenue = fields.Float('Minimum Revenue (VAT)')
    check_edit = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Check Edit', default='yes', compute='_compute_check_edit')
    real_revenue = fields.Float(string='Real Revenue', compute='_compute_real_revenue', store=False)
    create_month = fields.Integer('Create Month', compute='_compute_create_month', store=True)
    check_priority = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Check Priority', default='yes', compute='_compute_check_priority')

    @api.constrains('minimum_revenue')
    def _check_minimum_revenue(self):
        if self.minimum_revenue:
            if self.minimum_revenue < 0:
                raise ValidationError("The expected price must be strictly positive")

    # Check if count of sales order > 0, then minimum_revenue is readonly
    def _compute_check_edit(self):
        count_sale_order = self.env['sale.order'].search_count([('opportunity_id', '=', self.id)])
        self.check_edit = 'yes'
        if count_sale_order > 0:
            self.check_edit = 'no'

    # Calculate real_revenue = amount_total corresponding to the opportunity
    def _compute_real_revenue(self):
        for rec in self:
            if rec.name:
                amount_total = self.env['sale.order'].search([('opportunity_id', '=', rec.name)])
                amount_total_opportunity = amount_total.mapped('amount_total')
                rec.real_revenue = sum(amount_total_opportunity)

    @api.depends('create_date')
    def _compute_create_month(self):
        for rec in self:
            if rec.create_date:
                create_date = str(rec.create_date)
                create_month = create_date.split("-")
                rec.create_month = create_month[1]

    # Check priority = 3 then hide the Lost button
    @api.depends('priority')
    def _compute_check_priority(self):
        for rec in self:
            rec.check_priority = 'yes'
            if rec.priority == '3':
                rec.check_priority = 'no'

    # Override the Lost button again for the groups leader
    def btn_leader_set_lost(self):
        return super(SCrmLead, self).action_set_lost()
