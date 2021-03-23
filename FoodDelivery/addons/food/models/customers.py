from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, Warning
# class Customers(models.Model):
#     _name = 'customers.details'
#     _inherit = 'mail.thread'
#     _description = 'Customers details'
# #     _rec_name= 'name'
#     
#     GENDER_LIST = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
#     name= fields.Many2one('res.users')
#     mobile = fields.Char(related="name.mobile", readonly=False, track_visibility='onchange')
#     phone = fields.Char(related="name.phone", readonly=False)
#     email = fields.Char(related="name.email", readonly=False)
#     street = fields.Char(related="name.street", readonly=False)
#     street2 = fields.Char(related="name.street2", readonly=False)
#     zip = fields.Char(related="name.zip", readonly=False)
#     city = fields.Char(related="name.city", readonly=False)
#     country_id = fields.Many2one('res.country', related="name.country_id", readonly=False)
#     state_id = fields.Many2one('res.country.state', related="name.state_id", readonly=False)
# #     gender = fields.Selection(GENDER_LIST, required=True)
#     img = fields.Image()
# #     country_id = fields.Many2one('res.country')
# #     state_id =fields.Many2one('res.country.state')
#     #     To fetch the CUSTOMERS ORDERS
#     def my_orders(self):
#         print("Smart Button")
#         return{
#             'name': _('My Orders'),
#             'domain': [('name_id','=',self.id)],
#             'view_type': 'form',
#             'res_model': 'orders.details',
#             'view_id': False,
#             'view_mode': 'tree,form',
#             'type': 'ir.actions.act_window',
#         }


class Category(models.Model):
    _name = 'category.details'
    _inherit = 'mail.thread'
    _description = 'This is the table to store category details'
    
    name = fields.Char(required=True, track_visibility='always')
    count = fields.Integer(compute="_compute_count")
    
    
    def _compute_count(self):
        self.count = self.env['products.details'].search_count([('category_id', '=', self.id)])
    
     #     To fetch the CUSTOMERS ORDERS
    def fetch_prod(self):
        print("Smart Button")
        print(self.id)
        return{
            'name': _('Products in this Category'),
            'res_model': 'products.details',
            'domain': [('category_id','=',self.id)],
            'view_type': 'form',
            
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
