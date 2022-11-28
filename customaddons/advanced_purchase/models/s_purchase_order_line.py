from odoo import models, fields, api

class SPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)],
                                 change_default=True, index='btree_not_null')
    supplier = fields.Char('Supplier', compute='_compute_supplier')

    #Check supplier for cheapest price
    @api.depends('product_id')
    def _compute_supplier(self):
        for rec in self:
            supplier_line_price = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', rec.product_id.id)],
                                                                      order='price asc')
            supplier_price = supplier_line_price.mapped('partner_id.name')
            # Check supplier for shortest delivery time
            if len(supplier_price) > 1:
                supplier_line_delay = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', rec.product_id.id)],
                                                                          order='delay asc', limit=1)
                supplier_delay = supplier_line_delay.mapped('partner_id.name')
                for line in self:
                    line.supplier = ''.join(supplier_delay)
            else:
                for line in self:
                    line.supplier = ''.join(supplier_price)