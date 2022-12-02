from odoo import models, fields, api


class SSaleOrder(models.Model):
    _inherit = 'sale.order'

    plan_sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order')

    # Override
    def action_confirm(self):
        if self.plan_sale_order_id and self.plan_sale_order_id.check_confirm == 'yes':
            res = super(SSaleOrder, self).action_confirm()
            return res
        else:
            raise models.ValidationError('The business plan has not been added or approved yet')
