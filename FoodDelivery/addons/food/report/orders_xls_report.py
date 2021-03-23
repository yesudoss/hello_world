from odoo import models


class OrderXLS(models.AbstractModel):
    _name = 'report.food.orders_cust_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        print("XLS Report called")
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', })
        format_total = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        merge_format = workbook.add_format({'font_size': 20,'align': 'center', 'bold': True,  'italic': True})
        sheet = workbook.add_worksheet('Orders')
        
        row = 3
        col = 0
        # sheet.right_to_left()

#         sheet.set_column(3, 3, 50)

        sheet.merge_range('A1:H2', 'Food Orders', merge_format)
        sheet.set_column(0, 0, 20)
        sheet.write(2, 0, 'Name', format1)
#         sheet.write(3, 0, lines.name_id.name, format2)
        sheet.set_column(0, 1, 25)#         
        sheet.write(2,1, 'Street', format1)
#         sheet.write(3,1, lines.street, format2)
#       
        sheet.set_column(0, 1, 15)  
        sheet.write(2,2, 'City', format1)
#         sheet.write(3,2, lines.city, format2)
#         
        sheet.write(2,3, 'State', format1)
#         sheet.write(3,3, lines.state_id.name, format2)
#         
        sheet.write(2,4, 'Zip', format1)
#         sheet.write(3,4, lines.zip, format2)
#         
        sheet.write(2, 5, 'Total', format1)
#         sheet.write(3, 5, lines.amount_total)
#         
#         
#         for line in lines:
#             sheet.write(row, col,     line.name_id.name)
#             sheet.write(row, col + 1, line.street)
#             sheet.write(row, col + 2, line.city)
#             sheet.write(row, col + 3, line.state_id.name)
#             sheet.write(row, col + 4, line.zip)
#             sheet.write(row, col + 5, line.amount_total, format_total)
#             row += 1
