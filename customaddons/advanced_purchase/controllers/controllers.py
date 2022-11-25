# -*- coding: utf-8 -*-
# from odoo import http


# class AdvancedPurchase(http.Controller):
#     @http.route('/advanced_purchase/advanced_purchase', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/advanced_purchase/advanced_purchase/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('advanced_purchase.listing', {
#             'root': '/advanced_purchase/advanced_purchase',
#             'objects': http.request.env['advanced_purchase.advanced_purchase'].search([]),
#         })

#     @http.route('/advanced_purchase/advanced_purchase/objects/<model("advanced_purchase.advanced_purchase"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('advanced_purchase.object', {
#             'object': obj
#         })
