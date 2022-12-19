from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SCrmLead(models.Model):
    _inherit = 'crm.lead'

    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
    minimum_revenue = fields.Float('Minimum Revenue (VAT)')
    quotation_count = fields.Integer(compute='_compute_quotation_count', string="Quotations", store=False)
    is_minimum_revenue = fields.Boolean('Edit Minimum Revenue', default=False,
                                        compute='_compute_is_minimum_revenue', store=True)
    real_revenue = fields.Float(string='Real Revenue', compute='_compute_real_revenue', store=False)
    create_month = fields.Integer('Create Month', compute='_compute_create_month', store=True)
    is_priority = fields.Boolean('Is Priority', default=False, compute='_compute_is_priority', store=True)

    @api.constrains('minimum_revenue')
    def _check_minimum_revenue(self):
        if self.minimum_revenue:
            if self.minimum_revenue < 0:
                raise ValidationError("The expected price must be strictly positive")

    # Check if count of sales order > 0, then minimum_revenue is readonly
    def _compute_quotation_count(self):
        for rec in self:
            rec.quotation_count = 0
            if rec.id:
                quotation_count = self.env['sale.order'].search_count([('opportunity_id', '=', rec.id)])
                rec.quotation_count = quotation_count

    @api.depends('quotation_count')
    def _compute_is_minimum_revenue(self):
        for rec in self:
            if rec.quotation_count > 0:
                rec.is_minimum_revenue = True

    # Calculate real_revenue = amount_total corresponding to the opportunity
    def _compute_real_revenue(self):
        for rec in self:
            if rec.id:
                amount_total = self.env['sale.order'].search([('opportunity_id', '=', rec.id)])
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
    def _compute_is_priority(self):
        for rec in self:
            rec.is_priority = False
            if rec.priority == '3':
                rec.is_priority = True

    # Override the Lost button again for the groups leader
    def btn_leader_set_lost(self):
        return super(SCrmLead, self).action_set_lost()

    # Only assign opportunities to yourself or sales staff. Manager can sign for everyone
    @api.onchange('user_id')
    def _onchange_user_id(self):
        current_uid = self.env.uid

        employee_list_id = []
        employee_ids = self.env.ref('advanced_crm_sales.group_staff_employee').users.ids
        approver_ids = self.env.ref('advanced_crm_sales.group_staff_approver').users.ids
        manager_ids = self.env.ref('advanced_crm_sales.group_staff_manager').users.ids
        leader_ids = self.env.ref('advanced_crm_sales.group_staff_leader').users.ids

        for id in employee_ids:
            if id not in manager_ids and id not in leader_ids and id not in approver_ids:
                employee_list_id.append(id)

        if current_uid in employee_list_id:
            return {'domain': {'user_id': [('id', 'in', employee_list_id)]}}
