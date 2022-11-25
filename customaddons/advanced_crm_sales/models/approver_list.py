from odoo import fields, models

class AprroverList(models.Model):
    _name = 'approver.list'
    _description = 'Approver List'

    approver = fields.Many2one('res.partner', string='Approver')
    approval_status = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('refuse', 'Refuse'),
    ], string='Approval Status', default='draft', readonly=True)
    order_id = fields.Many2one('plan.sale.order', string='Order Reference', readonly=True)
    state_related = fields.Selection(related='order_id.state', string='State related')

# all approvers confirm approval or disapproval
    def btn_approve(self):
        self.approval_status = 'approve'
        states = self.order_id.order_line.mapped('approval_status')
        if all([state == 'approve' for state in states]):
            self.order_id.check_confirm = 'yes'


    def btn_refuse(self):
        self.approval_status = 'refuse'
        states = self.order_id.order_line.mapped('approval_status')
        if all([state == 'refuse' for state in states]):
            self.order_id.check_confirm = 'no'