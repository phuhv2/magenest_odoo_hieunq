from odoo import models, fields, api, _


class SSaleOrder(models.Model):
    _inherit = 'sale.order'

    plan_sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order')

    # Override check added plan and plan approved
    def action_confirm(self):
        if self.plan_sale_order_id and self.plan_sale_order_id.is_confirm == True:
            return super(SSaleOrder, self).action_confirm()
        else:
            raise models.ValidationError('The business plan has not been added or approved yet')
