from odoo import fields, models
from odoo.exceptions import UserError

class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _description = 'Plan Sale Order'
    _inherit = ['mail.thread']

    name = fields.Text(required=True, tracking=True)
    quotation = fields.Many2one('sale.order', store=True, required=True)
    content = fields.Text(string='Content of the quotations', required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('new', 'New'),
        ('send', 'Send'),
        ('approve', 'Approve'),
        ('refuse', 'Refuse'),
    ], string='State of quotation', readonly=True, tracking=True, default='draft')
    check_confirm = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ('new', 'New')
    ], tracking=True)
    order_line = fields.One2many('approver.list', 'order_id', string='Order Lines', tracking=True)

    # create new plan sale
    def btn_new(self):
        self.state = 'new'
        self.order_line.approval_status = 'draft'
        self.check_confirm = 'new'

    # send the plan to the approver
    def btn_send(self):
        noti_send = f'({self.create_uid.name}) {fields.Datetime.now()} -> The new plan has been sent.'

        if self.state == 'new':
            if self.order_line.approver:
                self.state = 'send'
                self.message_post(subject='Send to approver', body=noti_send, message_type='notification',
                                  partner_ids=self.order_line.approver.ids)
            else:
                raise UserError('Please write your approvers')
        else:
            raise UserError('Cannot confirm this approve')

    # approve confirm
    def btn_approve_confirm(self):
        noti_send = f'({self.create_uid.name}) {fields.Datetime.now()} -> The new plan has been approved.'

        if self.check_confirm == 'yes':
            if self.order_line.approver:
                self.state = 'approve'
                self.message_post(subject='Approve New Plan', body=noti_send)
            else:
                raise UserError('Please write your approvers.')
        else:
            raise UserError('All approvers have not yet agreed to approve.')

    # refuse confirm
    def btn_refuse_confirm(self):
        noti_send = f'({self.create_uid.name}) {fields.Datetime.now()} -> The new plan has been refused.'

        if self.check_confirm == 'no':
            self.state = 'refuse'
            self.message_post(subject='Refuse New Plan', body=noti_send)
        else:
            raise UserError('All approvers who have not yet declined approval.')