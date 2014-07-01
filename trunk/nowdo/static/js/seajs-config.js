/**
 * Created by SL on 14-4-29.
 */

seajs.config({

    // 别名配置
    alias: {
        '$': 'jquery/jquery/2.1.0/jquery',
        'nowdo': 'nowdo/nowdo/1.0.0/nowdo'
    },

    // 预加载项
    preload: [
        'seajs/seajs-text/1.0.2/seajs-text'
    ],

    // 文件编码
    charset: 'utf-8'
});

if(seajs.data.debug){
    seajs.config({
        alias: {
            "$": "jquery/jquery/2.1.0/jquery",
            "jquery": "jquery/jquery/2.1.0/jquery",
            'nowdo': '/static/js/nowdo/src/nowdo',
            'backbone': 'gallery/backbone/1.1.2/backbone',
            "summernote": "nowdo/summernote/0.5.2/summernote",
            "fancybox": "nowdo/fancybox/2.1.5/fancybox",
            'jquery-form': 'nowdo/jquery-form/3.20.0/jquery-form',
            'underscore': 'gallery/underscore/1.6.0/underscore',
            'bootstrap': 'gallery/bootstrap/3.0.0/bootstrap',
            "fileupload": "nowdo/fileupload/9.5.2/fileupload",
            "jquery-ui": "nowdo/jquery-ui/1.10.4/jquery-ui"
        }
    });
}