/**
 * Created by SL on 14-5-7.
 */

define(function(require, exports){
    exports.getCookie = function(name){
        if (document.cookie.length > 0){
            //先查询cookie是否为空，为空就return ""
            var c_start = document.cookie.indexOf(name + "=");
            if (c_start != -1){
                c_start = c_start + name.length + 1;
                var c_end=document.cookie.indexOf(";", c_start);
                if (c_end == -1)
                    c_end=document.cookie.length;
                return decodeURI(document.cookie.substring(c_start,c_end));
            }
        }
        return ""
    };

    exports.setCookie = function(name, value, expiredays){
        var date = new Date();
        expiredays = expiredays || 30;
        date.setDate(date.getDate() + expiredays);
        document.cookie = name + "=" + decodeURI(value) + ((expiredays == null) ? "" : ";expires=" + date.toUTCString());
    };
});
