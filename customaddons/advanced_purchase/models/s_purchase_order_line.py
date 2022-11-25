from odoo import models, fields, api

class SPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    supplier_info_ids = fields.Many2many('product.supplierinfo', 'purchase_order_line_product_supplierinfo_rel', 'partner_id',
                                   'product_id', string='Supplier Info List')

    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)],
                                 change_default=True, index='btree_not_null')
    supplier = fields.Char('Supplier', compute='_compute_supplier')

    # Check supplier for cheapest price
    @api.depends('product_id')
    def _compute_supplier(self):
        suppliers_price = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', self.product_id.id)], order='price asc')
        supplier_price = suppliers_price.mapped('partner_id.name')
        # Check supplier for shortest delivery time
        if len(supplier_price)>1:
            suppliers_delay = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', self.product_id.id)], order='delay asc', limit=1)
            supplier_delay = suppliers_delay.mapped('partner_id.name')
            for rec in self:
                rec.supplier = ''.join(supplier_delay)
        else:
            for rec in self:
                rec.supplier = ''.join(supplier_price)