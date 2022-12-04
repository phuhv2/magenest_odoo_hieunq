from odoo import fields, models, api, _


class SChoiceDepartment(models.TransientModel):
    _name = 's.choice.department'
    _description = 'Choice Department Wizard'

    month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', default='1', required=True)
    department_id = fields.Many2many('hr.department', string='Department')

    # Filter data by month and department name
    def btn_confirm(self):
        for rec in self:
            if rec.month and rec.department_id:
                return {
                    'name': _("Detail Report"),
                    'view_mode': 'tree',
                    'res_model': 'hr.department',
                    'type': 'ir.actions.act_window',
                    'view_id': self.env.ref('hr.view_department_tree').id,
                    'target': 'current',
                    'domain': [('create_month', '=', rec.month), ('name', '=', rec.department_id.mapped('name'))],
                    'context': {'create': False, 'edit': False, 'delete': False}
                }
            else:
                return {
                    'name': _("Detail Report"),
                    'view_mode': 'tree',
                    'res_model': 'hr.department',
                    'type': 'ir.actions.act_window',
                    'view_id': self.env.ref('hr.view_department_tree').id,
                    'target': 'current',
                    'context': {'create': False, 'edit': False, 'delete': False}
                }
