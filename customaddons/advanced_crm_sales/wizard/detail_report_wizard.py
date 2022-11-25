from odoo import fields, models, api, _
from datetime import date


class DetailReportWizard(models.TransientModel):
    _name = 'detail.report.wizard'
    _description = 'Detail Report Wizard'

    month = fields.Selection([
        ('0', date.today().strftime('%B')),
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', default='0')
    sales_team_id = fields.Many2one('crm.team', string='Sales Team')

# Display detailed report results by month and sales group
    def btn_confirm(self):
        if self.month and self.sales_team_id:
            return {
                'name': _("Detail Report"),
                'view_mode': 'tree',
                'res_model': 'crm.lead',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('advanced_crm_sales.crm_lead_wizard_extend_tree').id,
                'target': 'current',
                'domain': [('create_month', '=', self.month), ('sales_team', '=', self.sales_team_id.id)],
                'context': {'create': False, 'edit': False, 'delete': False}
            }
        else:
            return {
                'name': _("Detail Report"),
                'view_mode': 'tree',
                'res_model': 'crm.lead',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('advanced_crm_sales.crm_lead_wizard_extend_tree').id,
                'target': 'current',
                'context': {'create': False, 'edit': False, 'delete': False}
            }






    # tinh doanh thu thuc te actual_revenue bang tong price_total trong sale_order_line