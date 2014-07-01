/**
 * Created by SL on 14-4-30.
 */

define(function(require, exports, module){
    require('bootstrap');
    var $ = require('$'),
        Backbone = require('backbone'),
        _ = require('underscore');

    var BaseView = Backbone.View.extend({
        options: function(options){
            _.extend(this, options);
            return this;
        }
    });

    exports.ModalView = BaseView.extend({
        className: 'modal fade',
        template: _.template(require('./templates/modal-dialog.tpl')),

        setModalContent: function(content_view){
            content_view.setElement(this.$('.modal-body')).render();
            return this;
        },

        setTitle: function(modal_title){
            this.$('.modal-title').text(modal_title);
            return this;
        },

        setClass: function(extra_class){
            this.$('.modal-dialog').addClass(extra_class);
        },

        render: function(){
            this.$el.html(this.template());
            return this;
        },

        close: function(){
            this.$el.modal('hide');
        }
    })
});