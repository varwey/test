define(function(require, exports, module){
    require('bootstrap');
    var $ = require('$'),
        Backbone = require('backbone'),
        _ = require('underscore');

    var dropDownTemplate = require("./templates/drop_down_list.tpl");

    function highlighter(query, item, style) {
        if (query === "") {
            return item;
        }

        query = query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, "\\$&");
        return item.replace(new RegExp("(" + query + ")", "ig"), function($1, match) {
            return "<strong>" + match + "</strong>";
        });
    }

    exports.sugbox = function(selector, search_name){
        $.ajax({
            url: '/search/name_search',
            data: {'text': search_name},
            dataType: "json",
            success: function(res) {
                var tag_results = res.data.showed_tags;
                var task_results = res.data.showed_tasks;
                $(selector).html(_.template(dropDownTemplate)({
                    tag_results: tag_results,
                    task_results: task_results,
                    search_name: search_name,
                    hl: highlighter
                }))
                $(selector).slideDown();
            },
            error: function(xhr, status, error) {
                console.log(error)
            }
        });
    }
});