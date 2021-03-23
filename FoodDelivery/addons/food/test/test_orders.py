# -*- coding: utf-8 -*-
from odoo.tests import common

class TestOrders(common.TransactionCase):
    
    def setUp(self):
        super(TestOrders, self).setUp()

        self.category = self.env['category.details'].create({'name': 'Test'})
        self.product = self.env['products.details'].create({'name': 'Test Product', 'category_id': self.category.id})
#         self.institute = self.env['res.religious.institute'].create({'name': 'Test','founder':'Augustin','motto':'Thinking about Motto'})
#         self.region = self.env['res.religious.region'].create({'institute_id':self.institute.id,'name': 'Test'})
#         self.province = self.env['res.religious.province'].create({'institute_id':self.institute.id,'name': 'Test'})
        
    def test_check_province(self):
        self.assertEqual(self.category.id, self.product.category_id.id)
#         self.assertEqual(self.institute.id, self.province.institute_id.id)