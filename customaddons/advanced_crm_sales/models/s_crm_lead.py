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