from odoo import fields, models, api
from datetime import datetime
from odoo .exceptions import UserError
# from numpy import record

class DateReport(models.AbstractModel):
    _name = 'report.food.order_date_template'
    # here 'report.passengers.field.report' is folder_name, addon_name and template_name

    def get_data(self, form_values):
        data = []
        from_date = form_values['from_date']
        to_date = form_values['to_date']
        total_all = 0
        
# here we are using query to get data instead if search ORM         
        sql = """ SELECT 
                        od.order_seq, rp.name, od.phone, od.email, od.date_time, od.amount_total, od.status 
                    FROM 
                        orders_details as od 
                    LEFT JOIN 
                        res_partner as rp 
                    ON 
                        rp.id = od.name_id"""
        self.env.cr.execute(sql, (tuple(self.ids),))
        results = self.env.cr.dictfetchall()
        print("results")
        print(results)
        
        if form_values['from_date'] or form_values['to_date']:
            recordsets = self.env['orders.details'].search([('date_time', '>=', form_values['from_date']), ('date_time', '<=', form_values['to_date'])])
    
            print("recordsets")
            print(recordsets)
#         for rec in recordsets:
#             date_time = recordsets.date_time
        for obj in recordsets:
            if obj.status =='confirm' or 'received':
                if obj.amount_total:
                    total_all += obj.amount_total

#         for recordsets in recordsets:
#             data.append({
#                 'order_seq': recordsets.order_seq,
#                 'name': recordsets.name_id,
#                 'phone': recordsets.phone,
#                 'email': recordsets.email,
#                 'date': recordsets.date_time,
#                 'total': recordsets.amount_total,
#                 'total_all': total_all,
# #                 'from_date': recordsets.from_date,
# #                 'to_date': recordsets.to_date,
#             })
        for rec in results:    
            rec['total_all'] = total_all
        print(results)
        print(data)
        return results

    @api.model
    def _get_report_values(self, docsids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        return {
            'doc_ids': docsids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'get_data': self.get_data(data['form']),
        }