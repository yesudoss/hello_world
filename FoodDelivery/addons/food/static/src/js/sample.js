odoo.define('food.dashb', function (require) {
	"use strict";
	console.log("Hello World, sample js loaded");
	
	var AbstractAction = require('web.AbstractAction');
	var core = require('web.core');
	var FoodDash = AbstractAction.extend({
			    template: 'FoodClient',
			    init: function(parent, context){
			        console.log("INIT");
			        this._super(parent, context);
			        this.dashboards_templates = ['FoodDash'];
			    },
			    willStart: function(){
			        var self = this;
			        return self.fetch_data();
			    },
			    
			    fetch_data: function(){
			        console.log("Fetch")
			        var self = this;
			        var def1 = this._rpc({
			            model: 'products.details',
			            method : 'get_products_info',
			        }).then(function(result){
			               console.log(result)
			               self.data = result;
			        });
			        return $.when(def1);
			    },
	});
	core.action_registry.add('food_dash', FoodDash);
	return FoodDash;
});

