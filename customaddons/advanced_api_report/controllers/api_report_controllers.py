from odoo import http
from odoo.http import request
import json


class SalesPurchase(http.Controller):
    @http.route('/api-report', type='http', auth='none', methods=["POST"], csrf=False)
    def sales_purchase(self, **kwargs):
        body = json.loads(request.httprequest.data)
        access_token = "odooneverdie"

        if body["token"] == access_token and body["month"]:
            indicator_evaluation = request.env['indicator.evaluation'].sudo().search([('month', '=', body["month"])])
            sale_team_name = indicator_evaluation.mapped('sale_team_id.name')
            real_revenue = indicator_evaluation.mapped('real_revenue')
            real_revenue_difference = indicator_evaluation.mapped('real_revenue_difference')

            hr_department = request.env['hr.department'].sudo().search([('create_month', '=', body["month"])])
            department_name = hr_department.mapped('name')
            real_cost = hr_department.mapped('real_cost')
            real_cost_difference = hr_department.mapped('real_cost_difference')

            context = {
                "sales": [],
                "purchase": []
            }

            for name, real_revenue, diff in zip(sale_team_name, real_revenue, real_revenue_difference):
                context["sales"].append({
                    "sale_team_name": name,
                    "real_revenue": real_revenue,
                    "diff": diff
                })

            for name, real_cost, diff in zip(department_name, real_cost, real_cost_difference):
                context["purchase"].append({
                    "department_name": name,
                    "real_cost": real_cost,
                    "diff": diff
                })
        else:
            context = {
                "status": "The service is temporarily unavailable",
                "content": "The service in charge of the requested endpoint is temporarily unavailable or unreachable."
            }

        json_context = json.dumps(context, indent=4)
        return json_context
