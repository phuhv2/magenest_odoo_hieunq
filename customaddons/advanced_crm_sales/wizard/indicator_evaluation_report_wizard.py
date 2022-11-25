from odoo import fields, models, _
from datetime import date

class IndicatorEvaluationReportWizard(models.TransientModel):
    _name = 'indicator.evaluation.report.wizard'
    _description = 'Indicator Evaluation Report Wizard'

    month = fields.Selection([
        ('0', date.today().strftime('%B')),
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', default='0')
    sales_team_id = fields.Many2one('crm.team', string='Sales Team')


# Display monthly and sales group evaluation reports
    def btn_confirm(self):
        if self.month and self.sales_team_id:
            return {
                'name': _("Detail Report"),
                'view_mode': 'tree',
                'res_model': 'indicator.evaluation',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('advanced_crm_sales.indicator_evaluation_tree_view').id,
                'target': 'current',
                'domain': [('sales_team_ids', '=', self.sales_team_id.id)],
                'context': {'create': False, 'edit': False, 'delete': False}
            }
        else:
            return {
                'name': _("Detail Report"),
                'view_mode': 'tree',
                'res_model': 'indicator.evaluation',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('advanced_crm_sales.indicator_evaluation_tree_view').id,
                'target': 'current',
                'context': {'create': False, 'edit': False, 'delete': False}
            }


