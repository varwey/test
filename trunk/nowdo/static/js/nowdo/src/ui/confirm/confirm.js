/**
 * Created by SL on 14-5-7.
 */

define(function(require, exports){
    var Backbone = require('backbone'),
        _ = require('underscore'),
        $ = require('$');

    var ConfirmView = Backbone.View.extend({
        template: _.template(require('./templates/confirm.tpl')),

        className: 'modal fade',

        events: {
            'click .confirm-cancel': 'confirmCancel',
            'click .confirm-ok': 'confirmOK'
        },

        options: {
            title: '提示',
            content: ''
        },

        onCancel: function(callback){
            this.on_cancel_callback = callback;
            return this;
        },

        onOk: function(callback){
            this.on_ok_callback = callback;
            return this;
        },

        initialize: function(){
            $('body').append(this.$el.hide());
        },

        confirmCancel: function(){
            this.close();
            if(this.on_cancel_callback){
                this.on_cancel_callback();
            }
        },

        confirmOK: function(){
            this.close();
            if(this.on_ok_callback){
                this.on_ok_callback();
            }
        },

        render: function(){
            this.$el.html(this.template(this.options));
            return this;
        },

        show: function(options){
            this.options = _.extend(this.options, options);
            this.render().$el.modal({
                backdrop: 'static'
            });
        },

        close: function(){
            this.$el.modal('hide');
        }
    });

    var confirmView = new ConfirmView();

    exports.confirm = function(options){
        confirmView.show(options);
        return confirmView;
    };

    exports.activeTranslationConfirm = function(){
        return exports.confirm({
            content: require('./templates/open_translation_confirm.tpl')
        })
    };
});
