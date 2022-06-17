from odoo.exceptions import UserError
from odoo import models, fields
from datetime import datetime
import xlrd 
import base64

class CreateIvoicesByExcelData(models.TransientModel):
    _name = "create.invoice.by.excel.data"

    tag = fields.Char(string="Tag")
    document = fields.Binary(string="Document")
     
     
    def read_excel(self):

        """
        
        Читаем данные из эксель файла и подготавливаем словарь для создания счетов.

        """

        invoices = {}
        data = {}
        try:
            wb = xlrd.open_workbook(file_contents=base64.b64decode(self.document))
        except FileNotFoundError:
            raise UserError('Нет такого файла. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Нужно выбрать excel файл.')
        
        for sheet in wb.sheets():
            try:
                for row in range(1, sheet.nrows):
                    for col in range(sheet.ncols):
                        data_rows = sheet.cell(0,col).value
                        if col == 1:
                            data[data_rows] = (
                                datetime.utcfromtimestamp(
                                (sheet.cell(row,col).value - 25569) * 86400.0)
                                ).strftime('%Y-%m-%d')
                        else:
                            data[data_rows] = sheet.cell(row,col).value
                    invoice_number = sheet.cell(row,0).value
                    if invoice_number in invoices:
                        invoices[invoice_number].append(data.copy())
                    else:
                        invoices[invoice_number] = [data.copy()]
            except IndexError:
                raise UserError(
                    'Возможно данные в файле не соответстуют заданному формату.'
                    )
                pass
        self.make_invoices(invoices)


    def make_invoices(self, invoices):

        """ 

        Выбераем всех клиентов соответсвующих заданому тегу и создаем счета.

        """
        sql_query = 'select partner_id from res_partner_res_partner_category_rel '
        sql_query += 'where category_id=%s'
        try:
            self.env.cr.execute(
                 sql_query, 
                [self.env['res.partner.category'].search([('name', '=', self.tag)]).id]
                )
        except Exception:
            raise UserError('Убедитесь, что такой тэг\категория существует.')

        for i in self.env.cr.fetchall():
            partner = i[0]
            for invoice, goods in invoices.items():
                line_values =[]
                for good in goods:
                    product_id = self.env['product.product'].search(
                        [('default_code', '=', good["Артикул тарифа"])]
                        ).id
                    line_values.append((0, None, {
                        'product_id': product_id,
                        'quantity': good["Количество"],
                        'price_unit': good["Цена"],
                        'price_subtotal': good["Цена"],
                    }))
                self.env['account.move'].create([
                    {
                        'move_type': 'out_invoice',
                        'name': invoice,
                        'invoice_date': invoices[invoice][0]["Дата"], 
                        'partner_id': partner,
                        'currency_id': self.env.company.currency_id,
                        'invoice_line_ids': line_values,
                    },
                ])