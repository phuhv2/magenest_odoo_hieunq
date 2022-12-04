from odoo import fields, models, api, _
from datetime import date


class SReportCrmLead(models.TransientModel):
    _name = 's.report.crm.lead'

    month = fields.Selection([
        ('0', date.today().strftime('%B')),
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', default='0', required=True)
    sale_team_id = fields.Many2many('crm.team', string='Sale Team')

    # Filter data by sale_team, by selected month or by current month
    def btn_confirm(self):
        for rec in self:
            if rec.month and rec.sale_team_id:
                if rec.month == '0':
                    current_month = date.today().month
                sale_team = rec.sale_team_id.mapped('id')
                for id in sale_team:
                    return {
                        'name': _("Detail Report"),
                        'view_mode': 'tree',
                        'res_model': 'crm.lead',
                        'type': 'ir.actions.act_window',
                        'view_id': self.env.ref('crm.crm_case_tree_view_oppor').id,
                        'target': 'current',
                        'domain': [('sales_team_id', '=', id),
                                   '|', ('create_month', '=', rec.month),
                                        ('create_month', '=', current_month)],
                        'context': {'create': False, 'edit': False, 'delete': False}
                    }
            else:
                return {
                    'name': _("Detail Report"),
                    'view_mode': 'tree',
                    'res_model': 'crm.lead',
                    'type': 'ir.actions.act_window',
                    'view_id': self.env.ref('crm.crm_case_tree_view_oppor').id,
                    'target': 'current',
                    'context': {'create': False, 'edit': False, 'delete': False}
                }
