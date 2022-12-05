from odoo import fields, models, api, _
from datetime import date


class ReportIndicatorEvaluation(models.TransientModel):
    _name = 'report.indicator.evaluation'

    month = fields.Selection([
        ('0', date.today().strftime('%B')),
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', default='0', required=True)
    sale_team_id = fields.Many2many('crm.team', string='Sale Team')

    # Filter data by sale_team, by selected month or by current month
    def btn_confirm(self):
        if self.month and self.sale_team_id:
            if self.month == '0':
                self.month = str(date.today().month)
            sale_teams_id = self.sale_team_id.mapped('id')
            context =  {
                'name': _("Detail Report"),
                'view_mode': 'tree',
                'res_model': 'indicator.evaluation',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('advanced_crm_sales.indicator_evaluation_view_tree').id,
                'target': 'current',
                'domain': [('sale_team', 'in', sale_teams_id), ('create_month', '=', self.month)],
                'context': {'create': False, 'edit': False, 'delete': False}
            }

        else:
            context = {
                'name': _("Detail Report"),
                'view_mode': 'tree',
                'res_model': 'indicator.evaluation',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('advanced_crm_sales.indicator_evaluation_view_tree').id,
                'target': 'current',
                'context': {'create': False, 'edit': False, 'delete': False}
            }
        return context