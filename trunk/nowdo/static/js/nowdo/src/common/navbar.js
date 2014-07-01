define(function(require, exports){
    var login = require('../login/login'),
        alertView = require('../ui/alert/alert'),
        confirm = require('../ui/confirm/confirm'),
        sugbox = require('../ui/sugbox/sugbox').sugbox,
        _ = require('underscore'),
        $ = require('$');

    exports.addNavbarSearch = function(selector) {
        $(selector).after($("<ul>", {
            class: "search-dropdown",
            style: "display: none"
        }));

        $(selector).keyup(function(e){
            if(e.keyCode == 13) {
                e.preventDefault();
                var tag = $(this).val();

                if(!tag || !tag.trim()) {
                    return
                }

                window.location = '/tag?tag=' + tag.trim();
            } else {
                var text = $(this).val();

                if(!text || !text.trim()) {
                    $(".search-dropdown").slideUp();
                    return
                }

                sugbox(".search-dropdown", text.trim());
            }
        });

        $(selector).focus(function(e){
            var tag = $(this).val();

            if(!tag || !tag.trim()) {
                return
            }

            $(".search-dropdown").slideDown();
        })

        $(selector).blur(function(e){
            setTimeout(function() {
                $(".search-dropdown").slideUp();
            }, 200)
        })
    }

    exports.addClickNavbarSearchButton = function(selector) {
        $(selector).click(function(e){
            e.preventDefault();
            var tag = $('.navbar-search-input').val();

            if(!tag || !tag.trim()) {
                return
            }

            window.location = '/tag?tag=' + tag;
        });
    }
});
