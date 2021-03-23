from odoo import http, _
from odoo.http import request
import base64
from base64 import decode
import tempfile
import subprocess
import imghdr
import os, sys, time
#-------------------------This class is used to print Hello World-----------------------------------------------------------------------------------------
class HelloWorldController(http.Controller):
    @http.route('/hello/', auth='public')
    def index(self, **kw):
        return "Hello, Yesu"
    
    
#------------------------------------------------------------------------------------------------------------------

class FoodController(http.Controller):
# This class is used to fetch products data from DB and display it in tree view
    @http.route('/products/', auth='public', website=True)
    def index(self, **kw):
#                                             Model name
        product_data = http.request.env['products.details']
#                                     addon_name.template_id
        return http.request.render('food.product_template', {'prod_data': product_data.search([])})


#---------------------------This is to display the clicked products details widely---------------------------------
    @http.route(['/products/details/<model("products.details"):prod_data>'], auth='public', type='http', website=True)
    def details_product(self,prod_data):
        values={'prod_data': prod_data}
        return request.render("food.template_products_details",values )
    
            
#--------------------------To Delete record--------------------------------------------------------------------------------------------------------
    @http.route('/products/delete/<int:id>', type="http", auth='user', website=True, method=['GET','POST']) 
    def products_delete(self, access_token=None, report_type=None, download=False,**post_data): 
        if post_data['id']: 
            obj = request.env['products.details'].sudo().search([('id','=', post_data['id'])]) 
            obj.unlink()
            return http.redirect_with_hash('/')
#             return request.render("food.product_template")

#---------------------------This is for Edit an existing product------------------------------------------------------------------------------------
    @http.route('/products/edit/<int:id>', type='http', auth="public", website=True, csrf=False, methods=['GET', 'POST'])
    def edit_product(self, **kw):
        prod = request.env['products.details'].search([('id','=', kw['id'])])
        category_id = request.env['category.details'].search([])
        data = [category_id]
        return http.request.render('food.products_edit', {'data': data, 'prod':prod})

#--------------------------To is to save edited products records to products.details object---------------------------------------------------------------------------------------
    @http.route('/products/edit/save', type='http', methods=['POST'], auth="public", website=True, csrf=False)
    def products_edit_save(self, **kw):
        #here in kw you can get the inputted value
        name= kw['name']
#         img = kw['img']
#         ty = kw['type']
#         category_id = kw['category_id']
        cost = kw['cost']
#         description = kw['description']
#         category_id = request.env['category.details'].search([('id', '=', category_id)], limit=1)
        values = {'name': name,'cost': cost}
        request.env['products.details'].sudo().search([('id', '=', kw['id'])]).write(values)
        return http.request.render('food.template_thanks', {})
#         return "Thankyou !!"

#     def update_product(self):
#             print("Product details Updated")
#             for rec in self:
#                 return rec.product_id.write({'img': rec.img, 'type': rec.type, 'category_id': rec.category_id, 'cost': rec.cost, 'description': rec.description})

#---------------------------This is for create a new product------------------------------------------------------------------------------------
    @http.route('/products/create', type='http', auth="public", website=True, csrf=False, methods=['GET', 'POST'], sitemap=False)
    def create_product(self, **kw):
        category_id = request.env['category.details'].search([])
        data = [category_id]
        return http.request.render('food.products_create', {'data': data})
    
    
#--------------------------To is to save products records to products.details object---------------------------------------------------------------------------------------
    @http.route('/products/create/save', type='http', methods=['POST'], auth="public", website=True, csrf=False)
    def products_save(self, **kw):
        #here in kw you can get the inputted value
        name= kw['name']
        img = kw['img']
        ty = kw['type']
        category_id = kw['category_id']
        cost = kw['cost']
        description = kw['description']
        category_id = request.env['category.details'].search([('id', '=', category_id)], limit=1)
        values = {'name': name, 'type': ty, 'img': img.read().decode('base64'),'category_id': kw['category_id'], 'cost': cost, 'description': description}
        request.env['products.details'].sudo().create(values)
        return http.request.render('food.template_thanks', {})
#         return "Thankyou !!"

#--------------------------This is for create feedback-------------------------------------------------------------------------------------
    @http.route('/feedback', type='http', auth="public", website=True, csrf=False)
    def create_feedback(self, **kw):
        return http.request.render('food.template_create_feedback')
    
#-------------------------Thanks Page-----------------------------------------------------------------------------------------------------------
#       This is for create a new product
    @http.route('/thanks', type='http', auth="public", website=True, csrf=False)
    def thanks(self, **kw):
        return http.request.render('food.template_thanks')
       
#----------------------------------------------------------------------------------------------------------------------