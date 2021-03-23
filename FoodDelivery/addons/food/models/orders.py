from odoo import fields, models, api, _, tools
from datetime import datetime
from odoo.exceptions import ValidationError, Warning
from odoo.addons.base.models.ir_mail_server import MailDeliveryException
from odoo.osv import expression
from lxml import etree
import json

class Orders(models.Model):
    
    _name = 'orders.details'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'This is the table to store order details'
    _rec_name = 'name_id'
    
    
    STATUS_LIST = [('draft', 'Draft'), ('cancel', 'Cancel'), ('confirm', 'Confirm'), ('received', 'Received')]
    
    
#     name = fields.Char(required=True, track_visibility='always')
#     name_id = fields.Many2one('customers.details', )
    name_id= fields.Many2one('res.partner')
    phone = fields.Char(related="name_id.phone", readonly=False, store=True)
    email = fields.Char(related="name_id.email", readonly=False, store=True)
    street = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state')
    
    order_seq = fields.Char(string="Order Reference", required=True, readonly=True, copy=False,
                           index=True, default=lambda self: _('New'))
    status = fields.Selection(STATUS_LIST, required=True, default='draft')
    date_time = fields.Datetime(default=datetime.now(), readonly=True)
    currency_id = fields.Many2one('res.currency')
    order_line_ids = fields.One2many('orderline.details', 'order_id', track_visibility='always')
    amount_total = fields.Monetary(compute='_amount_all', readonly=True, store=True)
    
    is_same = fields.Boolean(string="Same as customer's address")
    
    
    
# ---------------------CONSTRAINS DEOCRATOR for EMAIL Validation-----------------------------------------------
#     @api.constrains('mail')
#     def validate_mail(self):
#         if self.mail and not tools.single_email_re.match(self.mail):
#             raise ValidationError("Email is not valid")
#     
#-----------------------This is to send invoice through email---------------------------------------------------
    def action_send_invoice(self):
        template_id = self.env.ref('food.food_order_email_template').id
#                                     addon_name.template id
        template = self.env['mail.template'].browse(template_id)
#         try:
        template.send_mail(self.id, force_send=True)
#         except:
#             raise ValidationError(_("Delivery Failed"))

#             raise MailDeliveryException(_("Delivery Failed"))
    
#-------------------------------------------------------------

    def mail_sending_template(self):
        print("Cron is called")
#         register_ids = self.env['orders.details'].search([('date_time', '=', datetime.datetime.today())])
        register_ids = self.env['orders.details'].search([])
        for rec in register_ids:
            print(rec.email)
            email_to = rec.email
            email_template = self.env.ref('food.food_order_good_morning_email_template')
            if email_to:
                email_template.send_mail(rec.id,force_send=True)

#         for register_id in register_ids:
#             email_to = register_id.email
#             email_template = self.env.ref('car_project.email_sending_customer')
#             if email_to:
#                 email_template.send_mail(self.id,force_send=True)

#----------------------- DEFAULT_GET ORM------------------------------------------------------------------
    @api.model
    def default_get(self, fields):
        data = super(Orders, self).default_get(fields)
        # train_id = self.env['train.details'].search([('train_code', '=', '101')])
        # if train_id:
        #     data['train_id'] = train_id.id

#         classing_id = self.env['classing.details'].search([('class_code', '=', '1A')])
#         if classing_id:
#             data['classing_id'] = classing_id.id

        country_id = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
        state_id = self.env['res.country.state'].search([('country_id', '=', country_id.id), ('code', '=', 'TN')],
                                                        limit=1)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        if state_id:
            data['state_id'] = state_id.id
        if country_id:
            data['country_id'] = country_id.id or []
        # data['gender'] = 'male'
        return data
    
#------------------------  To fetch Products and show----------------------------------------------------------- 
    def fetch_products(self):
        print("Fetch Products called")
        return{
            'name': _('Products'),
#             'domain': [('name','=',self.id)],
            'view_type': 'kanban',
            'res_model': 'products.details',
            'view_id': False,
            'view_mode': 'kanban',
            'type': 'ir.actions.act_window',
        }
    
#------------------------ ONCHANGE DECORATOR--------------------------------------------------------------------
    @api.onchange('is_same')
    def _onchange_is_same(self):
            if self.is_same:
                for obj in self.name_id:
                    self.update({
                        'street' : obj.street, 'city': obj.city, 'state_id': obj.state_id, 'zip': obj.zip, 'country_id': obj.country_id})
            else:
                self.update({'street' : "", 'city': "", 'zip': "",})
    
#--------------------- NAME_GET ORM for Override rec_name--------------------------------------------------------
    def name_get(self):
        result = []
        for rec in self:
            if rec.name_id and rec.order_seq:
                name_id = rec.name_id.name + ' - ' + rec.order_seq
                result.append((rec.id, name_id))
        return result
    
#-------------------------To calculate Total---------------------------------------------------------------------    
    @api.depends('order_line_ids.sub_total')
    def _amount_all(self):
        print('Total Calculated')
        self.amount_total = False
        for rec in self:
            
            total =  0
            for line in rec.order_line_ids:
                total += line.sub_total
                rec.update({
                'amount_total': total,
                })
    
#---------------------- DEFAULT_GET ORM for COUNTRY and STATE and CURRENCY------------------------------------
#     @api.model
#     def default_get(self, fields):
#         data = super(Orders, self).default_get(fields)
#         currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
#         if currency_id:
#             data['currency_id'] = currency_id.id
#         return data

#---------------------- CREATE ORM FOR SEQUENCE-----------------------------------------------------------------
    @api.model
    def create(self, vals):
        if vals.get('order_seq', _('New')) == _('New'):
            vals['order_seq'] = self.env['ir.sequence'].next_by_code('order.sequence') or _('New')
        result = super(Orders, self).create(vals)
        return result
    
#-----------------------UNLINK ORM------------------------------------------------------------------------------
    def unlink(self):
        for rec in self:
            if rec.status in ['confirm', 'received']:
                raise ValidationError(_("You cannot delete these confirmed/Received records"))
            return super(Orders, self).unlink()

#-----------------------------------------------------------------

    @api.model
    def tracking_fields(self):
        print("Tracking field called")
        result = super(Orders, self).tracking_fields()
        result.append([
        # ("URL_PARAMETER", "FIELD_NAME_MIXIN", "NAME_IN_COOKIES")
            ('name_id', 'name_id', 'odoo_utm_my_field')
        ])
        return result

#------------------------ THIS IS for STATUS BAR-------------------------------------------------------------------
    def action_draft(self):
        if self.status:
            print(self.status)
            self.status = "draft"
    def action_confirm(self):
        if self.status:
            print(self.status)
            self.status = "confirm"
            self.message_post(body=_('Dear %s , Your order has been Confirmed.') % (self.name_id.name,))
    def action_cancel(self):
        if self.status:
            print(self.status)
            self.status = "cancel"
            self.message_post(body=_('Dear %s , Your order has been Cancelled :(.') % (self.name_id.name,))
    def action_received(self):
        if self.status:
            print(self.status)
            self.status = "received"
            self.message_post(body=_('Dear %s , Your order has been delivered.') % (self.name_id.name,))
            self.message_post_with_view('hr_expense.hr_expense_template_refuse_reason',
                                             values={'status': self.status, 'is_sheet': False, 'name': self.name_id.name})

#             self.message_post(body="Status received")
#             self.message_post(self, body='', subject=None, message_type='notification', subtype=None, parent_id=False, attachments=None, **kwargs)
    
        # # FIELDS_VIEW_GET ORM
    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(Passenger, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                  submenu=submenu)
    #     doc = etree.XML(res['arch'])
    #
    #     if self.user_has_groups("passengers.passengers_passenger_role"):
    #         if view_type == 'form':
    #             # Remove the if statement if you want to make changes in every view
    #             for node in doc.xpath("//field[@name='status']"):
    #                 modifiers = json.loads(node.get('modifiers'))
    #                 modifiers['readonly'] = True
    #                 node.set("modifiers", json.dumps(modifiers))
    #
    #         res['arch'] = etree.tostring(doc, encoding='unicode')
    #         return res

    
            
class OrderLine(models.Model):
    _name = 'orderline.details'
    _description = 'Order Line'
    _rec_name = 'product_id'
    
    
    product_id = fields.Many2one('products.details', string="Product", required=True)
    currency_id = fields.Many2one('res.currency')
    cost = fields.Monetary(related='product_id.cost', string="Cost")
    quantity = fields.Integer(string="Quantity", default=1)
    sub_total = fields.Monetary(compute='_calculate_subotal', readonly=True, store=True)
    order_id = fields.Many2one('orders.details', string="Ordering Customer")
    
    @api.depends('cost', 'quantity')
    def _calculate_subotal(self):
        avl_qt = 0
        for rec in self:
            if rec.cost and rec.quantity:
                rec.sub_total = rec.cost * rec.quantity
# #                 avl_qt = rec.env['products.details'].search([('id', '=', rec.product_id.id)], limit=1)
#                 rec.avl_qt = rec.product_id.available_quantity - rec.quantity
# #                 avl_qt = avl_qt.available_quantity - rec.quantity
#                 print("Available Quantity is ", rec.avl_qt)
#                 rec.product_id.write({'available_quantity': rec.avl_qt})
# #                 return self.search['products.details'].sudo.search([('id', '=', rec.product_id.id)]).write({'available_quantity': avl_qt})
# #                 search.env['products.details'].sudo().search([('id', '=', kw['id'])]).write()
                
# ---------------------CONSTRAINS DEOCRATOR for UOM-----------------------------------------------
    @api.constrains('quantity')
    def validate_uom(self):
        for rec in self:
            if rec.quantity:
                rec.avl_qt = rec.product_id.available_quantity - rec.quantity
                print(rec.avl_qt)
                rec.product_id.write({'available_quantity': rec.avl_qt})

#------------------------ ONCHANGE DECORATOR to validate quantity is available or not--------------------------------------------------------------------
    @api.constrains('quantity')
    def _onchange_quantity(self):
        avl_qt = 0
        for rec in self:
            if rec.quantity:
                rec.avl_qt = rec.product_id.available_quantity - rec.quantity
                if rec.quantity >= rec.avl_qt:
                    raise ValidationError(_("Low stock"))
                    
#-------------------- DEFAULT_GET ORM for COUNTRY and STATE and CURRENCY--------------------------------------
    @api.model
    def default_get(self, fields):
        data = super(OrderLine, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        return data