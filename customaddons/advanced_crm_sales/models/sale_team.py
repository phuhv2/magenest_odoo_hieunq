from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MonthlySales(models.Model):
    _inherit = "crm.team"

    january_sales = fields.Float("January Sales", digits=(12, 3))
    february_sales = fields.Float("February Sales", digits=(12, 3))
    march_sales = fields.Float("March Sales", digits=(12, 3))
    april_sales = fields.Float("April Sales", digits=(12, 3))
    may_sales = fields.Float("May Sales", digits=(12, 3))
    june_sales= fields.Float("June Sales", digits=(12, 3))
    july_sales = fields.Float("July Sales", digits=(12, 3))
    august_sales = fields.Float("August Sales", digits=(12, 3))
    september_sales = fields.Float("September Sales", digits=(12, 3))
    october_sales = fields.Float("October Sales", digits=(12, 3))
    november_sales = fields.Float("November Sales", digits=(12, 3))
    december_sales = fields.Float("December Sales", digits=(12, 3))

    @api.constrains('january_sales', 'february_sales', 'march_sales', 'april_sales', 'may_sales', 'june_sales',
                    'july_sales', 'august_sales', 'september_sales', 'october_sales', 'november_sales', 'december_sales')
    def _check_month(self):
        for rec in self:
            if (rec.january_sales<0 and rec.february_sales<0 and rec.march_sales<0 and rec.april_sales<0
                    and rec.may_sales<0 and rec.june_sales<0 and rec.july_sales<0 and rec.august_sales<0
                    and rec.september_sales<0 and rec.october_sales<0 and rec.november_sales<0 and rec.december_sales<0):

                raise ValidationError("The expected price must be strictly positive")


