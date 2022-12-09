# -*- coding: utf-8 -*-
# from odoo import http


# class AdvancedApiReport(http.Controller):
#     @http.route('/advanced_api_report/advanced_api_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/advanced_api_report/advanced_api_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('advanced_api_report.listing', {
#             'root': '/advanced_api_report/advanced_api_report',
#             'objects': http.request.env['advanced_api_report.advanced_api_report'].search([]),
#         })

#     @http.route('/advanced_api_report/advanced_api_report/objects/<model("advanced_api_report.advanced_api_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('advanced_api_report.object', {
#             'object': obj
#         })
