from odoo import fields, models, api

class SChoiceDepartment(models.TransientModel):
    _name = 's.choice.department'
    _description = 'Choice Department Wizard'

    month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', default='1', required=True)
    department_id = fields.Many2many('hr.department', string='Department')

    def btn_confirm(self):
        pass
