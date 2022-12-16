from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SCrmTeam(models.Model):
    _inherit = 'crm.team'

    january_sales = fields.Float("January Sales")
    february_sales = fields.Float("February Sales")
    march_sales = fields.Float("March Sales")
    april_sales = fields.Float("April Sales")
    may_sales = fields.Float("May Sales")
    june_sales = fields.Float("June Sales")
    july_sales = fields.Float("July Sales")
    august_sales = fields.Float("August Sales")
    september_sales = fields.Float("September Sales")
    october_sales = fields.Float("October Sales")
    november_sales = fields.Float("November Sales")
    december_sales = fields.Float("December Sales")

    @api.constrains('january_sales', 'february_sales', 'march_sales', 'april_sales', 'may_sales', 'june_sales',
                    'july_sales', 'august_sales', 'september_sales', 'october_sales', 'november_sales',
                    'december_sales')
    def _check_month(self):
        if (self.january_sales < 0 or self.february_sales < 0 or self.march_sales < 0 or self.april_sales < 0
                or self.may_sales < 0 or self.june_sales < 0 or self.july_sales < 0 or self.august_sales < 0
                or self.september_sales < 0 or self.october_sales < 0 or self.november_sales < 0 or self.december_sales < 0):
            raise ValidationError("The expected price must be strictly positive")
