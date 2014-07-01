/**
 * Created by SL on 14-4-30.
 */
define(function(require, exports, module){

    var Backbone = require('backbone'),
        _ = require('underscore'),
        $ = require('$');

    var AlertView = Backbone.View.extend({
        template: _.template(require('./templates/alert.tpl')),
        className: 'alert-xc',

        initialize: function(){
            this.options = {
                category: 'danger',
                info: ''
            };
            this.$el.hide();
            $('body').append(this.el);
        },

        events: {
            'click .close': 'close'
        },

        show: function(options){
            this.options = options;
            this.render().$el.fadeIn();
            setTimeout($.proxy(this.close, this), 2000);
        },

        close: function(){
            this.$el.fadeOut();
        },

        render: function(){
            this.$el.html(this.template(this.options));
            return this;
        }
    });

    var alertView = new AlertView();

    exports.alert = function(options){
        alertView.show(options);
    }
});

