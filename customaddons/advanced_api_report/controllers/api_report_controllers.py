from odoo import http
from odoo.http import request
import json


class SalesPurchase(http.Controller):
    @http.route('/api-report', type='http', auth='none', methods=["POST"], csrf=False)
    def SalesPurchase(self, **kwargs):
        body = json.loads(request.httprequest.data)
        token = "odooneverdie"

        if body["token"] == token and body["month"]:
            indicator_evaluation = request.env['indicator.evaluation'].sudo().search([('month', '=', body["month"])])
            sale_team = indicator_evaluation.mapped('sale_team_id')
            sale_teams = sale_team.mapped('name')
            real_revenue = indicator_evaluation.mapped('real_revenue')
            revenue_difference = indicator_evaluation.mapped('revenue_difference')

            hr_department = request.env['hr.department'].sudo().search([('create_month', '=', body["month"])])
            name = hr_department.mapped('name')
            department_real_revenue = hr_department.mapped('real_revenue')
            department_revenue_difference = hr_department.mapped('revenue_difference')

            context = {
                "sales": [],
                "purchase": []
            }

            for sale_team_name, real_revenue, diff in zip(sale_teams, real_revenue, revenue_difference):
                context["sales"].append({
                    "sale_team_name": sale_team_name,
                    "real_revenue": real_revenue,
                    "diff": diff
                })

            for department_name, real_cost, diff in zip(name, department_real_revenue, department_revenue_difference):
                context["purchase"].append({
                    "department_name": department_name,
                    "real_cost": real_cost,
                    "diff": diff
                })
        else:
            context = {
                "status": "The service is temporarily unavailable",
                "content": "The service in charge of the requested endpoint is temporarily unavailable or unreachable."
            }

        json_obj = json.dumps(context, indent=4)
        return json_obj
