from odoo import models, fields
from odoo.exceptions import UserError

class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _inherit = ['mail.thread']

    name = fields.Text('Plan Sale Order Name', required=True)
    quotation = fields.Many2one('sale.order', string='Quotation', readonly=True)
    content = fields.Text(string='Content', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('send', 'Send'),
        ('approve', 'Approve'),
        ('refuse', 'Refuse'),
    ], string='State')
    approver_id = fields.One2many('approver.list', 'plan_sale_order_id', string='Approver')
    check_confirm = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Check Confirm')

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
        if self.check_confirm == 'yes':
            if self.approver_id.approver:
                self.state = 'approve'
                self.message_post(body=f'{self.create_uid.name} -> The new plan has been approved.')
            else:
                raise UserError('Please write your approvers.')
        else:
            raise UserError('All approvers have not yet agreed to approve.')

    # refuse confirm
    def btn_refuse_confirm(self):
        if self.check_confirm == 'no':
            self.state = 'refuse'
            self.message_post(body=f'{self.create_uid.name}-> The new plan has been refused.')
        else:
            raise UserError('All approvers who have not yet declined approval.')