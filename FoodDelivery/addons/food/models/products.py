from odoo import fields, models, api, _
from odoo.osv import expression
from odoo.exceptions import ValidationError, Warning
class Customers(models.Model):
    _name = 'products.details'
    _inherit = 'mail.thread'
    _description = 'Products details'
#     _rec_name= 'name'
    
    STATUS_LIST = [('available', 'Available'), ('not_available', 'Not Available')]
    TYPE_LIST = [('veg', 'Vegetarian'), ('non_veg', 'Non-Vegetarian')]
    
    
    name= fields.Char()
    img = fields.Binary()
    status = fields.Selection(STATUS_LIST, required=True, default='not_available' , track_visibility='onchange')
    type = fields.Selection(TYPE_LIST, required=True, default='veg')
    category_id = fields.Many2one('category.details', required=True, ondelete="cascade")
    currency_id = fields.Many2one('res.currency')
    cost = fields.Monetary()
    description = fields.Html()
    count = fields.Char(string="Count", compute="_compute_count")
    available_quantity = fields.Integer()

    def server_status_available(self):
        for rec in self:
            if rec.status =='not_available':
                rec.action_available()
            
    
#     NAME SEARCH ORM for searching food products using name and category
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('category_id', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))

    
    # This is for Client Action II by Pradison
    @api.model
    def get_products_info(self):
        # print(self)
        print("get_products_info method called for client action")
        value = []
        data = self.env['products.details'].search([])
        print(data)
        for rec in data:
            value.append({'name': rec.name, 'type': rec.type,'category': rec.category_id.name ,'cost': rec.cost, 'status': rec.status})
        print(value)
        return value
    
    
# DEFAULT_GET ORM for COUNTRY and STATE and CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(Customers, self).default_get(fields)
        # classing_id = self.env['classing.details'].search([('class_code', '=', '1A')])
        # if classing_id:
        #     data['classing_id'] = classing_id.id

        # status_id = self.env['pay.details'].search([('status', '=', 'paid')])

#         country_id = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
#         state_id = self.env['res.country.state'].search([('country_id', '=', country_id.id), ('code', '=', 'TN')],
#                                                         limit=1)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id

#         if state_id:
#             data['state_id'] = state_id.id
#         print(state_id)
#         if country_id:
#             data['country_id'] = country_id.id or []
        return data
    
    # Search Count ORM / COMPUTE COUNT ORM
    def _compute_count(self):
        # BROWSE ORM
        # unt = self.browse()
        # print(unt)
        self.count = self.env['orderline.details'].search_count([('product_id', '=', self.id)])

        # ros = self.env['passenger.details'].browse(self.ids).read(fields)
        # for r in ros:
        #     record = self.browse(r['id'])
        #     record._update_cache({k: v for k, v in r.items() if k in fields}, validate=False)

# ---------------------CONSTRAINS DEOCRATOR for EMAIL Validation-----------------------------------------------
    @api.constrains('cost')
    def validate_cost(self):
        print('cost validated')
        if self.cost:
            for rec in self:
                print(rec.cost)
                if rec.cost <0.00 or not rec.cost:
                    raise ValidationError("Please Enter a valid cost")
    
#----------------------- THIS IS for STATUS BAR-----------------------------------------------------------------
    def action_not_available(self):
        if self.status:
            print(self.status)
            self.status = "not_available"
    def action_available(self):
        if self.status:
            print(self.status)
            self.status = "available"
