from odoo import api, models, tools, fields, _

class ProductUpdateWizard(models.TransientModel):
    _name = 'productupdate.wizard'
    _description = "This is the table for Product update wizard"
    # _rec_name = 'route_id'

    STATUS_LIST = [('available', 'Available'), ('not_available', 'Not Available')]
    TYPE_LIST = [('veg', 'vegetarian'), ('non_veg', 'Non-Vegetarian')]
    
    product_id = fields.Many2one('products.details', string="Product Name")
    currency_id = fields.Many2one('res.currency', string="Currency Type")
    cost = fields.Monetary(string="Cost")
    # # reservation_fee = fields.Integer(string="Reservation Fee (GST)")

    # DEFAULT_GET ORM for CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(ProductUpdateWizard, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
            return data

    def update_product(self):
        print("Product details Updated")
        for rec in self:
            return rec.product_id.write({'cost': rec.cost})
