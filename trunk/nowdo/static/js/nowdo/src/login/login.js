/**
 * Created by SL on 14-4-29.
 */

define(function(require, exports, module){
    require('jquery-form');
    var $ = require('$'),
        Modal = require('../ui/modal/modal'),
        Backbone = require('backbone'),
        alertView = require('../ui/alert/alert'),
        _ = require('underscore');

    var LoginFormView = Backbone.View.extend({
        login_template: _.template(require('./templates/login.tpl')),
        register_template: _.template(require('./templates/register.tpl')),
        register_success_template: _.template(require('./templates/register_success.tpl')),
        reset_pwd_template: _.template(require('./templates/forget_password.tpl')),
        reset_pwd_success_template: _.template(require('./templates/forget_password_success.tpl')),
        not_active_template: _.template(require('./templates/not_active.tpl')),

        events: {
            'click .change-status': 'changeStatus',
            'submit form': 'onSubmit'
        },

        _getTemplate: function(){
            switch (this.model.get('status')){
                case 'login':
                    return this.login_template;
                    break;
                case 'register':
                    return this.register_template;
                    break;
                case 'reset_pwd':
                    return this.reset_pwd_template;
                    break;
                default :
                    return false;
            }
        },

        _getTitle: function(){
            switch (this.model.get('status')){
                case 'login':
                    return '用户登录';
                    break;
                case 'register':
                    return '注册新用户';
                    break;
                case 'reset_pwd':
                    return '重置密码';
                    break;
                default :
                    return false;
            }
        },

        onSubmit: function(){
            return false;
        },

        configAjaxForm: function(){
            this.$('form').ajaxForm({
                success: $.proxy(function(res){
                    if(res.status === 'ok'){

                        if(this.model.get('status') === 'login'){
                            if(this.callback){
                                this.callback(res.data);
                                modalView.close();
                            }else{
                                location.reload();
                            }
                        }

                        else if(this.model.get('status') === 'register'){
                            this.$el.html(this.register_success_template(res.data))
                        }

                        else if(this.model.get('status') === 'reset_pwd'){
                            this.$el.html(this.reset_pwd_success_template(res.data))
                        }

                    }else{
                        if(this.model.get('status') === 'login' && res.info === 'not_active'){
                            this.$el.html(this.not_active_template(res.data));
                        }else{
                            this.$('.text-danger').text(res.info);
                        }
                    }
                }, this)
            });
        },

        render: function(){
            var template = this._getTemplate();
            this.$el.html(template(this.model.toJSON()));
            this.changeTitle();
            this.configAjaxForm();
            return this;
        },

        fadeRender: function(){
            var template = this._getTemplate();
            this.$el.fadeOut($.proxy(function(){
                this.$el.html(template(this.model.toJSON())).fadeIn();
                this.configAjaxForm();
            }, this));
            this.changeTitle();
            return this;
        },

        setModel: function(model){
            this.model = model;
            this.model.on('change:status', this.fadeRender, this);
        },

        setCallback: function(callback){
            this.callback = callback;
        },

        changeTitle: function(){
            modalView.setTitle(this._getTitle());
        },

        changeStatus: function(e){
            this.model.set('status', $(e.currentTarget).data('target_status'));
        }
    });

    var loginFormView = new LoginFormView(),
        modalView = new Modal.ModalView();

    $('body').append(modalView.render().el);

    var _openModal = function(status, title){
        return function(callback){
            loginFormView.setModel(new Backbone.Model({
                status: status,
                title: title
            }));
            if(callback){
                loginFormView.setCallback(callback);
            }
            modalView.setModalContent(loginFormView).setClass('modal-login');
            modalView.$el.modal();
        };
    };

    var _logout = function(callback){
        var url = '/account/ajax_logout';
        $.get(url, function(res){
            if(res.status === 'ok'){
                callback(res.data);
            }else{
                alertView.alert(res);
            }
        });
    };

    exports.logout = _logout;
    exports.openLoginModal = _openModal('login', '用户登录');
    exports.openRegisterModal = _openModal('register', '注册新用户');
    exports.openForgetPasswordModal = _openModal('reset_pwd', '重置密码');
});
