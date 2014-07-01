/**
 * Created by SL on 14-5-8.
 */

define(function(require, exports){

    /**
     * 过滤掉标签
     * @param html_str
     */
    exports.strip_tags = function(html_str){
        return html_str
            //将 p/div/br 标签结束位置添加换行符
            .replace(/(<\/p[^>]*>|<\/div[^>]*>|<br\/?>)/gi, '$1\n')
            //移除所有的标签
            .replace(/<!--.*?-->|<[^>]*>/g, '');
    };


    /**
     * 转义html标签
     * @param html_str
     */
    exports.escape = function(html_str){
        return html_str.replace(/&/g, '&amp;')
            .replace(/>/g, '&gt;')
            .replace(/</g, '&lt;')
            .replace(/\'/g, '&#39;')
            .replace(/\"/g, '&#34;')
    };

    /**
     * 转义除了 exclude html标签
     * @param html_str
     * @param exclude 正则表达式
     * @returns {*}
     */
    exports.escape_exclude = function(html_str, exclude){
        if(!exclude){
            return exports.escape(html_str);
        }
        var exclude_matched = html_str.match(exclude),
            exclude_split = html_str.split(exclude),
            res = '';

        for(var index in exclude_split){
            res += exports.escape(exclude_split[index]);
            if(index < exclude_matched.length){
                res += exclude_matched[index];
            }
        }
        return res
    };
});
