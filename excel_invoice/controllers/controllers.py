# -*- coding: utf-8 -*-
# from odoo import http


# class ExcelInvoice(http.Controller):
#     @http.route('/excel_invoice/excel_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/excel_invoice/excel_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('excel_invoice.listing', {
#             'root': '/excel_invoice/excel_invoice',
#             'objects': http.request.env['excel_invoice.excel_invoice'].search([]),
#         })

#     @http.route('/excel_invoice/excel_invoice/objects/<model("excel_invoice.excel_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('excel_invoice.object', {
#             'object': obj
#         })
