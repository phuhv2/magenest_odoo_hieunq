from odoo import fields, models, api, _

class SReportCrmLead(models.TransientModel):
    _name = 's.report.crm.lead'

    month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', default='1', required=True)
    sale_team_id = fields.Many2many('crm.team', string='Sale Team')

    def btn_confirm(self):
        for rec in self:
            if rec.month and rec.sale_team_id:
                sale_team = rec.sale_team_id.mapped('id')
                for id in sale_team:
                    return {
                        'name': _("Detail Report"),
                        'view_mode': 'tree',
                        'res_model': 'crm.lead',
                        'type': 'ir.actions.act_window',
                        'view_id': self.env.ref('crm.crm_case_tree_view_oppor').id,
                        'target': 'current',
                        'domain': [('create_month', '=', rec.month), ('sales_team_id', '=', id)],
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