/**
 * Created by SL on 14-4-29.
 */

define(function(require, exports, module){
    var $ = require('$'),
        alertView = require('../ui/alert/alert'),
        login = require('../login/login');

    function ajax_request(options){
        var url = options.url,
            data = options.data,
            callback = options.callback,
            success = options.success;

        $.get(url, data, function(res){
            if(!!success && success instanceof Function){
                if(res.status === 'ok'){
                    success(res.data);
                }else if(res.info === 'not_login'){
                    login.openLoginModal();
                }else{
                    alertView.alert(res);
                }
            }else{
                if(callback instanceof Function){
                    callback(res);
                }
            }
        });
    }

    exports.toggle_join_group = function(group_id, success){
        var url = '/group/' + group_id + '/toggle_join';
        ajax_request({
            url: url,
            success: success
        });
    };

    exports.toggle_follow_user = function(user_id, callback){
        var url = '/follow/toggle_follow_user';
        ajax_request({
            url: url,
            data: {
                target_id: user_id
            },
            callback: callback
        });
    };

    exports.like_user = function(target_id, callback){
        var url = '/like/like_task';
        ajax_request({
            url: url,
            data: {
                target_id: target_id
            },
            callback: callback
        });
    };

    exports.toggle_mark_as_featured_task = function(task_id, tag_id, success){
        var url = '/management/mark_as_featured_task';
        ajax_request({
            url: url,
            data: {
                task_id: task_id,
                tag_id: tag_id
            },
            success: success
        });
    };

    exports.toggle_active_task = function(task_id, success){
        var url = '/task/toggle_active_task';
        ajax_request({
            url: url,
            data: {
                task_id: task_id
            },
            success: success
        });
    };

    exports.logout = function(success){
        var url = '/account/ajax_logout';
        ajax_request({
            url: url,
            success: success
        });
    };

    exports.get_user_info = function(user_id, success){
        var url = '/account/get_user_info';
        var data = null;
        if(typeof user_id === 'object'){
            data = user_id
        }else{
            data = {
                user_id: user_id
            }
        }
        ajax_request({
            url: url,
            data: data,
            success: success
        });
    };
});