/**
 * Created by SL on 14-4-29.
 */

define(function(require, exports, module){

    var Backbone = require('backbone'),
        _ = require('underscore'),
        $ = require('$');

    var CommentCollection = Backbone.Collection.extend({
        url: '/task/comments',

        parse: function(res){
            return res.data;
        }
    });

    var commentTemplate = _.template(require('./templates/comment.tpl'));
    var CommentListView = Backbone.View.extend({
        template: _.template(require('./templates/comment-list.tpl')),

        initialize: function(){
            this.commentCollection = new CommentCollection();
            this.commentCollection.on('reset', this.addComments, this);
        },

        events: {
            'click .close-comments': 'closeComments',
            'click .btn-comment': 'submitComment'
        },

        submitComment: function(e){
            var url = '/task/ajax_create_comment',
                comment_editor = this.$('.div-input'),
                comment_content = comment_editor.html(),
                task_id = this.model.get('task_id'),
                trigger = $(e.currentTarget);

            trigger.button('loading');

            $.ajax({
                url: url,
                type: 'post',
                data: {
                    task_id: task_id,
                    comment_content: comment_content
                },
                success: $.proxy(function(res){
                    if(res.status == 'ok'){
                        var comment = $(commentTemplate(res.data)).hide();
                        this.$('.media-list').prepend(comment);
                        comment.fadeIn();
                        $(trigger_map[task_id]).find('.comment-count').text(res.data.comment_count);
                        comment_editor.empty();
                    }else{
                        //TODO 改为更友好的错误提示
                        alert(res.info);
                    }
                }, this),
                complete: $.proxy(function(){
                    trigger.button('reset');
                    $('#loading').fadeOut();
                }, this)
            });
        },

        addComments: function(collection){
            var comment_container = this.$('.media-list');
            collection.each(function(model){
                comment_container.append(commentTemplate(model.toJSON()));
            });
        },

        closeComments: function(){
            var self = this;
            this.$el.slideUp(function(){
                self.$el.empty();
                self.active = false;
            });
        },

        render: function(){
            this.$el.html(this.template(this.model.toJSON())).slideDown('fast');
            return this;
        },

        activeTarget: function(task_id){
            var comment_list_ele = $('#comment-list-' + task_id);
            this.setElement(comment_list_ele);
            if(this.active){
                this.closeComments();
            }else{
                this.render().fetchCommentList();
                this.active = true;
            }
        },

        fetchCommentList: function(){
            this.commentCollection.fetch({data: {
                task_id: this.model.get('task_id')
            }, reset: true});
        }
    });

    var comment_list_view_map = {},
        trigger_map = {};

    exports.addCommentListTrigger = function(selector){
        $(selector).click(function(e){
            var trigger = e.currentTarget,
                target_id = $(trigger).data('target_id'),
                commentListView = comment_list_view_map[target_id];

            trigger_map[target_id] = trigger_map[target_id] || [];
            trigger_map[target_id].push(trigger);

            if(!commentListView){
                commentListView = new CommentListView({
                    model: new Backbone.Model({
                        task_id: target_id
                    })
                });
                comment_list_view_map[target_id] = commentListView;
            }
            commentListView.activeTarget(target_id);
        });
    };
});