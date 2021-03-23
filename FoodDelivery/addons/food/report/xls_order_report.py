from odoo import models


class OrdersXLSReport(models.AbstractModel):
    _name = 'report.food.ordered_cust_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', })
        sheet = workbook.add_worksheet('register cars')

        # sheet.right_to_left()

        sheet.set_column(3, 3, 50)
        sheet.set_column(2, 2, 30)
        sheet.write(2, 2, 'Name', format1)
#         sheet.write(2, 3, lines.customer_id.name, format2)
        sheet.write(3, 2, 'Car', format1)
#         sheet.write(3, 3, lines.car.name_car, format2)
        sheet.write(4, 2, 'From Date', format1)
#         sheet.write(4, 3, lines.from_date, format2)
        sheet.write(5, 2, 'End date', format1)
#         sheet.write(5, 3, lines.end_date, format2)
        sheet.write(6, 2, 'cost', format1)
#         sheet.write(6, 3, lines.cost, format2)
        sheet.write(7, 2, 'Total amount', format1)
#         sheet.write(7, 3, lines.total_amount, format2)