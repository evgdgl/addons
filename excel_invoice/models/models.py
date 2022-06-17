# -*- coding: utf-8 -*-

from odoo import models, fields, api


class excel_invoice(models.Model):
    _name = 'excel_invoice.excel_invoice'
    _description = 'excel_invoice.excel_invoice'


    def wizard_open(self):
        return {'type': 'ir.actions.act_window',
                'res_model': 'create.invoice.by.excel.data',
                'view_mode': 'form',
                'target': 'new'}
