from odoo import fields, models, api, _
from datetime import datetime
class Payment(models.Model):
    _name = 'payment.details'
    _inherit = 'mail.thread'
    _description = 'Payment details'
    _rec_name= 'order_id'

    
    STATUS_LIST = [('draft', 'Draft'), ('done', 'Done')]
    
    order_id = fields.Many2one('orders.details', string="Customer", ondelete="restrict")
    total = fields.Monetary(related="order_id.amount_total")
    payment_seq = fields.Char(string="Payment Reference", required=True, readonly=True, copy=False,
                           index=True, default=lambda self: _('New'))
    status = fields.Selection(STATUS_LIST, required=True, default='draft')
    date_time = fields.Datetime(default=datetime.now(), readonly=True)
    currency_id = fields.Many2one('res.currency')
    status_id = fields.Selection(related="order_id.status", readonly=False)
    
    
    # DEFAULT_GET ORM for CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(Payment, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        return data
    
    
        # Search Count ORM / COMPUTE COUNT ORM



#     @api.multi 
#     def _get_count_list(self):
#         data_obj    = self.env['example.object']
#         for data in self:       
#                list_data        = data_obj.search([('Fill the condition')])
#                data.example_count = len(list_data)


    
    
    
     # CREATE ORM FOR PAYMENT SEQUENCE
    @api.model
    def create(self, vals):
        if vals.get('order_seq', _('New')) == _('New'):
            vals['payment_seq'] = self.env['ir.sequence'].next_by_code('payment.sequence') or _('New')
        result = super(Payment, self).create(vals)
        return result
    
     # THIS IS for PAYMENT STATUS BAR
    def action_draft(self):
        if self.status:
            print(self.status)
            self.status = "draft"
            
    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'done':
            self.status_id = 'confirm'
#     def action_done(self):
#         if self.status:
#             print(self.status)
#             self.status = "done"