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

    def btn_confirm(self):
        for rec in self:
            if rec.month and rec.sale_team_id:
                sale_team = rec.sale_team_id.mapped('id')
                for id in sale_team:
                    return {
                        'name': _("Detail Report"),
                        'view_mode': 'tree',
                        'res_model': 'indicator.evaluation',
                        'type': 'ir.actions.act_window',
                        'view_id': self.env.ref('advanced_crm_sales.indicator_evaluation_view_tree').id,
                        'target': 'current',
                        'domain': [('create_month', '=', rec.month), ('sale_team', '=', id)],
                        'context': {'create': False, 'edit': False, 'delete': False}
                    }
            else:
                return {
                    'name': _("Detail Report"),
                    'view_mode': 'tree',
                    'res_model': 'indicator.evaluation',
                    'type': 'ir.actions.act_window',
                    'view_id': self.env.ref('advanced_crm_sales.indicator_evaluation_view_tree').id,
                    'target': 'current',
                    'context': {'create': False, 'edit': False, 'delete': False}
                }
