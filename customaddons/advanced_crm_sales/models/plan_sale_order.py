from odoo import models, fields, api
from odoo.exceptions import UserError


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _inherit = ['mail.thread']

    name = fields.Text(string='Plan Sale Order Name', required=True)
    quotation = fields.Many2one('sale.order', string='Quotation', readonly=True)
    content = fields.Text(string='Content', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('send', 'Send'),
        ('approve', 'Approve'),
        ('refuse', 'Refuse'),
    ], string='State')
    approver_id = fields.One2many('approver.list', 'plan_sale_order_id', string='Approver')
    is_confirm = fields.Boolean()
    is_send = fields.Boolean(compute='_compute_is_send')

    def btn_new(self):
        self.state = 'new'
        self.approver_id.approval_status = 'not approved yet'

    def btn_send(self):
        if self.state == 'new':
            if self.approver_id.approver:
                self.state = 'send'
                self.approver_id.approval_status = 'not approved yet'
                self.message_post(body=f'{self.create_uid.name} -> The new plan has been sent.')
            else:
                raise UserError('Please write your approvers')
        else:
            raise UserError('Cannot confirm this approve')

    def btn_approve_confirm(self):
        if self.is_confirm == True:
            if self.approver_id.approver:
                self.state = 'approve'
                self.message_post(body=f'{self.create_uid.name} -> The new plan has been approved.')
            else:
                raise UserError('Please write your approvers.')
        else:
            raise UserError('All approvers have not yet agreed to approve.')

    def btn_refuse_confirm(self):
        if self.is_confirm == False:
            self.state = 'refuse'
            self.message_post(body=f'{self.create_uid.name}-> The new plan has been refused.')
        else:
            raise UserError('All approvers who have not yet declined approval.')

    # Only the creator can use the send button
    def _compute_is_send(self):
        current_uid = self.env.uid
        create_uid = self.create_uid
        create_uid_result = create_uid.mapped('id')

        self.is_send = False
        if current_uid != create_uid_result[0]:
            self.is_send = True
