import requests
from odoo import http
from odoo.http import request
import json

class Sale(http.Controller):
    @http.route('/test', type='http', auth='none', methods=["POST"], csrf=False)
    def sale_details(self, **kwargs):
        params = request.params

        indicator_evaluation = request.env['indicator.evaluation'].sudo().search([])
        sale_team = indicator_evaluation.mapped('sale_team_id')
        sale_teams = sale_team.mapped('name')
        real_revenue = indicator_evaluation.mapped('real_revenue')
        revenue_difference = indicator_evaluation.mapped('revenue_difference')


        hr_department = request.env['hr.department'].sudo().search([])
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

        json_object = json.dumps(context, indent=4)
        return json_object

