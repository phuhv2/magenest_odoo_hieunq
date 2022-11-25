from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    plan_sale_order = fields.Many2one('plan.sale.order', string='Plan Sale Order')
    plan_sale_order_id = fields.One2many('plan.sale.order', 'quotation', string='Plan Sale Order Id')
    new_quotation = fields.Many2one(related='plan_sale_order_id.quotation')
    new_state = fields.Selection(related='plan_sale_order_id.state')
    real_revenue = fields.Float(string='Real Revenue', compute='_compute_actual_revenue', digits=(12, 3))

# check quotes and plans
    def action_confirm(self):
        if not self.new_quotation or self.new_state != 'approve':
            raise models.ValidationError('The business plan has not been added or approved yet')
        return super(SaleOrder, self).action_confirm()