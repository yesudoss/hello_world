odoo.define('busreservation.railway', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var rpc = require('web.rpc');
var session = require('web.session');
var web_client = require('web.web_client');
//var fieldRegistry = require('web.field_registry');
var _t  = core._t;
//var fieldUtils = require('web.field_utils');
var QWeb = core.qweb;

var FoodDashboard = AbstractAction.extend({
    template: 'FoodClientAction',

    init: function(parent, context){
        console.log("INIT");
        this._super(parent, context);
        this.dashboards_templates = ['FoodDashboard'];
    },

    willStart: function(){
        var self = this;
        return self.fetch_data();
    },

    start: function(){
        console.log("Start")
        var self = this;
        this.set("title", 'Dashboard');
        return this._super().then(function(){
//            self.$el.parent().addClass('oe_background_grey');
        });
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


//    cssLibs: [],
//    jsLibs: [],
//    events: [],
});
core.action_registry.add('food_dashboard', FoodDashboard);
return FoodDashboard;
});