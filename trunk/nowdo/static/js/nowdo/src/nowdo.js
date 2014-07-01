define(function(require, exports, module) {
    var $ = require('$');
    module.exports = {
        login: require('./login/login'),
        comment: require('./comment/comment'),
        publisher: require('./publisher/publisher'),
        trigger: require('./trigger/trigger'),
        alertView: require('./ui/alert/alert'),
        confirmView: require('./ui/confirm/confirm'),
        sugbox: require('./ui/sugbox/sugbox'),
        translateTool: require('./translate-tool/translate-tool'),
        navbar: require('./common/navbar')
    };

    $(function(){
        var alertView = module.exports.alertView;
        $.ajaxSetup({
            global: true,
            cache: false,
            beforeSend: function(jqxhr, setting){
                $('#loading').fadeIn();
            },

            complete: function(jqxhr, textStatus){
                $('#loading').fadeOut();
            },

            dataFilter: function(data){
                return data;
            },

            statusCode: {
                400: function(){
                    alertView.alert({category:'danger', info: '资源加载失败'});
                },
                404: function(){
                    alertView.alert({category: 'danger', info: '您访问的资源不存在'});
                },
                403: function(){
                    alertView.alert({category:'danger', info: '您无权进行此操作'});
                },
                500: function(){
                    alertView.alert({category:'danger', info: '操作失败'});
                }
            }
        });

        require('bootstrap');
        require('summernote');
        require('fancybox');

        $('a[data-toggle=tooltip]').tooltip();
    })
});