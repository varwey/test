/**
 * Created by SL on 14-4-29.
 */

define(function (require, exports, module) {

    var api = require('../api/api'),
        login = require('../login/login'),
        alertView = require('../ui/alert/alert'),
        confirm = require('../ui/confirm/confirm'),
        _ = require('underscore'),
        $ = require('$');

    var toggle_config = {
        default: {
            icon: ['fa-plus', 'fa-minus'],
            clazz: ['btn-success', 'btn-info']
        },
        join_group: {
            btn_text: ['加入小组', '退出小组'],
            clazz: false
        },
        mark_as_featured: {
            btn_text: ['加入精选', '取消精选']
        },
        active_task: {
            btn_text: ['开启翻译', '关闭翻译'],
            icon: ['fa-check-circle', 'fa-minus-circle']
        },
        horizontal_join_group: {
            icon: ['fa-plus-square', 'fa-minus-square'],
            btn_text: ['加入小组', '退出小组'],
            clazz: false
        }
    };

    function toggleButtonStatus($target, key, status) {
        var status_config = _.extend(toggle_config['default'], toggle_config[key]),
            cur_status_index = status + 0,
            opz_status_index = (cur_status_index + 1) % 2,
            clazz = status_config['clazz'],
            icon = status_config['icon'],
            btn_text = status_config['btn_text'];

        if (clazz) {
            $target.removeClass(clazz[opz_status_index]).addClass(clazz[cur_status_index]);
        }
        $target.find('i').removeClass(icon[opz_status_index]).addClass(icon[cur_status_index]);
        $target.find('.btn-text').text(btn_text[cur_status_index]);

        if (btn_text) {
            alertView.alert({category: 'success', info: btn_text[opz_status_index] + "成功"});
        }
    }

    exports.addLikeTrigger = function (selector) {
        $(selector).click(function (e) {
            var target = $(e.currentTarget),
                target_id = target.data('target_id');

            api.like_user(target_id, function (res) {
                if (res.status === 'ok') {
                    if (res.data && res.data.ret === 'like') {
                        target.addClass('active').find('i').removeClass('fa-heart-o').addClass('fa-heart');
                    } else {
                        target.removeClass('active').find('i').addClass('fa-heart-o').removeClass('fa-heart');
                    }
                    target.find('.like-count').text(res.data.like_count);
                } else {
                    if (res.info === 'not_login') {
                        login.openLoginModal();
                    }
                    alertView.alert(res);
                }
            });
        });
    };

    exports.addLoginTrigger = function (selector) {
        $(selector).click(function () {
            login.openLoginModal();
        });
    };

    exports.addRegisterTrigger = function (selector) {
        $(selector).click(function () {
            login.openRegisterModal();
        });
    };

    exports.addToggleJoinGroupTrigger = function (selector) {
        $(selector).click(function () {
            var $target = $(this),
                group_id = $target.data('group_id');
            api.toggle_join_group(group_id, function (joined) {
                toggleButtonStatus($target, 'join_group', joined);
            });
        });
    };

    exports.addToggleHorizontalJoinGroupTrigger = function (selector) {
        $(selector).click(function () {
            var $target = $(this),
                group_id = $target.data('group_id');
            api.toggle_join_group(group_id, function (joined) {
                toggleButtonStatus($target, 'horizontal_join_group', joined);
            });
        });
    };

    var default_data = {
        iconOnly: false,
        iconStyle: null
    };

    exports.addToggleFollowUserTrigger = function (selector) {
        var target = typeof selector === 'string' ? $(selector) : selector;
        target.off('click').click(function (e) {
            e.preventDefault();
            var $target = $(this),
                user_id = $target.data('user_id'),
                clazz = $target.attr('class'),
                follow_template = require('./templates/follow.tpl'),
                un_follow_template = require('./templates/un_follow.tpl');
            $target.button('loading');
            api.toggle_follow_user(user_id, function (res) {
                if (res.status === 'ok') {
                    var new_ele = null;
                    if (res.info === 'followed') {
                        new_ele = $(_.template(un_follow_template)(_.defaults($target.data(), default_data)));
                    } else {
                        new_ele = $(_.template(follow_template)(_.defaults($target.data(), default_data)));
                    }
                    new_ele.addClass(clazz);
                    new_ele.insertAfter($target);
                    exports.addToggleFollowUserTrigger('.follow');
                    $target.remove();
                    if (res.info === 'followed') {
                        alertView.alert({category: 'success', info: '取消关注成功'});
                    } else {
                        alertView.alert({category: 'success', info: '关注成功'});
                    }
                } else {
                    if (res.info === 'not_login') {
                        login.openLoginModal();
                        $target.button('reset');
                    } else {
                        alertView.alert(res)
                    }
                }
            });
        });
    };

    exports.addToggleHorizontalFollowUserTrigger = function (selector) {
        var target = typeof selector === 'string' ? $(selector) : selector;
        target.off('click').click(function (e) {
            e.preventDefault();
            var $target = $(this),
                user_id = $target.data('user_id'),
                clazz = $target.attr('class'),
                follow_template = require('./templates/horizontal_follow.tpl');
            $target.button('loading');
            api.toggle_follow_user(user_id, function (res) {
                if (res.status === 'ok') {
                    var new_ele = null;
                    if (res.info === 'followed') {
                        $target.remove();
                        alertView.alert({category: 'success', info: '关注成功'});
                    } else {
                        new_ele = $(_.template(follow_template)(_.defaults($target.data(), default_data)));
                        new_ele.addClass(clazz);
                        new_ele.insertAfter($target);
                        exports.addToggleFollowUserTrigger('.follow-user');
                        $target.remove();
                    }
                } else {
                    if (res.info === 'not_login') {
                        login.openLoginModal();
                        $target.button('reset');
                    } else {
                        alertView.alert(res)
                    }
                }
            });
        });
    };

    exports.addFeaturedTrigger = function (selector, tag_id) {
        $(selector).click(function () {
            var $target = $(this);
            api.toggle_mark_as_featured_task($target.data('task_id'), tag_id, function (featured) {
                toggleButtonStatus($target, 'mark_as_featured', featured);
            })
        });
    };

    exports.addToggleActiveTaskTrigger = function (selector) {
        $(selector).click(function (e) {
            e.stopPropagation();
            var $target = $(this),
                task_id = $target.data('task_id');
            api.toggle_active_task(task_id, function (actived) {
                toggleButtonStatus($target, 'active_task', actived);
            });
        });
    };

    exports.addUserInfoPopOverTrigger = function (selector) {
        $(selector)
            .mouseover(function () {
                var $target = $(this),
                    email = $target.data('email'),
                    user_id = $target.data('user_id');
                api.get_user_info({user_id: user_id, email: email}, function (user) {
                    var popover_content = $(_.template(require('./templates/user_info_pop.tpl'))(user));
                    $target.popover({
                        content: popover_content,
                        placement: 'auto top',
                        html: true,
                        container: 'body',
                        template: '<div class="popover user-info-popover"><div class="arrow"></div><div class="popover-inner"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
                    }).popover('show');
                    popover_content.mouseleave(function () {
                        $target.popover('destroy');
                    });
                    exports.addToggleFollowUserTrigger(popover_content.find('.follow'));
                });
            });
    };

    exports.addLinkToTargetUrl = function (selector) {
        $(selector).click(function (e) {
            e.preventDefault();
            e.stopPropagation();
            location.href = $(this).data('target-url');
        });
    };

    exports.addToggleExpandTrend = function (selector) {
        $(selector).click(function (e) {
            e.preventDefault();

            var trend_body_elem;
            var found = false,
                $node = $(e.target);
            do {
                if ($node.hasClass('trend-body')) {
                    found = true;
                    break;
                }
                $node = $node.parent();
            } while ($node != null);
            if (!found) {
                return;
            }

            trend_body_elem = $node;

            if (trend_body_elem.attr("data-status") == "close") {
                trend_body_elem.find(".part-text").addClass("hide");
                trend_body_elem.find(".full-text").removeClass("hide");
                trend_body_elem.attr("data-status", "open");
                trend_body_elem.find(".expand-trend").html('收起 <i class="fa fa-angle-up"></i>');
            } else {
                trend_body_elem.find(".part-text").removeClass("hide");
                trend_body_elem.find(".full-text").addClass("hide");
                trend_body_elem.attr("data-status", "close");
                trend_body_elem.find(".expand-trend").html('展开 <i class="fa fa-angle-down"></i>');

                var old_top = $("body").scrollTop();
                var new_top = trend_body_elem.parent().offset().top;

                if (old_top > new_top) {
                    $("body").scrollTop(new_top);
                }
            }
        });
    }
});
