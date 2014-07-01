/**
 * Created by SL on 14-3-13.
 */

define(function(require, exports){
    var Backbone = require('backbone'),
        _ = require('underscore'),
        $ = require('$'),
        login = require('../login/login'),
        trigger = require('../trigger/trigger'),
        cookie = require('../utils/cookie'),
        alertView = require('../ui/alert/alert');

    ZeroClipboard.config({
        moviePath: '/static/js/lib/zeroclipboard/ZeroClipboard.swf',
        swfPath: '/static/js/lib/zeroclipboard/ZeroClipboard.swf',
        forceHandCursor: true
    });
    var zero_client = new ZeroClipboard();

    var TOOL_TYPE_READ = 'read',
        TOOL_TYPE_TRANSLATE = 'translate',
        TOOL_TYPE_APPROVE = 'approve',

        READ_MODE_ORIGIN = 'origin',
        READ_MODE_COMPARE = 'compare',
        READ_MODE_RESULT = 'result';

    var current_tar_lang = null,
        router = null,
        task = null,
        supported_languages = null,
        current_read_mode = READ_MODE_ORIGIN,
        user = null;

    var url_map = {
        'fetch_entry_url': '/translate/fetch_entries',
        'add_trans_result': '/translate/add_trans_result',
        'other_result_url': '/translate/other_results',
        'up_vote_url': '/translate/up_vote',
        'approve_result_url': '/translate/approve',
        'fetch_glossary_url': '/translate/fetch_glossaries',
        'fetch_glossary_table_url': '/translate/fetch_glossary_table',
        'fetch_comment_url': '/task/comments',
        'submit_comment_url': '/task/ajax_create_comment',
        'create_glossary': '/translate/create_glossary',
        'collect_glossary_url': '/translate/collect_glossary'
    };

    var is_completed = function(tar_lang){
        return _.contains(task['completed_lang_list'], tar_lang);
    };

    var BaseCollection = Backbone.Collection.extend({
        parse: function(res){
            return res.data;
        }
    });

    var EntryModel = Backbone.Model.extend({
        parse: function(res){
            return _.extend(res, {
                read_mode: current_read_mode
            })
        }
    });

    var EntryCollection = BaseCollection.extend({
        model: EntryModel,
        url: url_map.fetch_entry_url,

        initialize: function(){
            this.current_editor_index = 0;
        },

        openCurrentEditor: function(){
            if(this.length > this.current_editor_index){
                entryCollection.at(this.current_editor_index).trigger('open-editor-event');
            }
        }
    });

    var GlossaryCollection = BaseCollection.extend({
        url: url_map.fetch_glossary_url
    });

    var GlossaryTableCollection = BaseCollection.extend({
        url: url_map.fetch_glossary_table_url,
        parse: function(res){
            return res.data;
        }
    });

    var OtherResultCollection = BaseCollection.extend({
        url: url_map.other_result_url
    });

    var CommentCollection = BaseCollection.extend({
        url: url_map.fetch_comment_url
    });

    var BaseView = Backbone.View.extend({
        options: function(options){
            _.extend(this, options);
            return this;
        }
    });

    var OtherResultView = BaseView.extend({
        tagName: 'li',
        className: '',
        template: _.template(require('./templates/other_result_item.tpl')),

        events: {
            'click .up-vote': 'upVote',
            'click .approve': 'approveResult'
        },

        initialize: function(){
            this.model.on('change', this.render, this);
        },

        approveResult: function(){
            this.editor.doApproveResult(this.model.toJSON());
        },

        upVote: function(e){
            $.get(url_map.up_vote_url, {result_id: this.model.id}, $.proxy(function(res){
                if(res.status === 'ok'){
                    this.model.set(res.data);
                }else{
                    alertView.alert(res);
                }
            }, this))
        },

        render: function(){
            this.$el.html(this.template(_.extend(this.model.toJSON(), {toolType: this.editor.toolType})));
            trigger.addUserInfoPopOverTrigger(this.$('.user-info-pop'));
            return this;
        }
    });

    var BaseEditorView = BaseView.extend({

        default_events: {
            'click .show-other-results': 'showOtherResult'
        },

        extra_events: {

        },

        initialize: function(){
            this.model.on('change', this.render, this);
            this.otherResultCollection = new OtherResultCollection();
            this.otherResultCollection.on('reset', this.addOtherResults, this)
        },

        events: function(){
            return _.defaults(this.default_events, this.extra_events);
        },

        nextEntry: function(){
            var current_position = parseInt(this.model.get('position'));

            if(current_position === entryCollection.length - 1){
                alertView.alert({category: 'info', info: '已经是最后一个'});
                return;
            }

            entryCollection.at(current_position + 1).trigger('open-editor-event');
        },

        preEntry: function(){
            var current_position = parseInt(this.model.get('position'));
            if(current_position === 0){
                alertView.alert({category: 'info', info: '已经是第一个'});
                return;
            }
            entryCollection.at(current_position - 1).trigger('open-editor-event');
        },

        showOtherResult: function(){
            if(this.otherResultShowed){
                this.$(".other-results").slideUp();
                this.otherResultShowed = false;
                return;
            }
            this.otherResultCollection.fetch({
                data: {
                    task_id: task.id,
                    entry_id: this.model.get('entry').id,
                    tar_lang: current_tar_lang,
                    with_mine: this.toolType === TOOL_TYPE_APPROVE
                },
                reset: true
            });
        },

        addOtherResults: function(collection){
            var otherResultsContainer = this.$(".other-results").empty();
            if(collection.length <= 0){
                otherResultsContainer.append($('<li/>').addClass('list-group-item').html('没有更多的翻译结果'));
            }else{
                collection.each(function(model){
                    var otherResultView = new OtherResultView({
                        model: model
                    });
                    otherResultView.options({
                        editor: this
                    });
                    otherResultsContainer.append(otherResultView.render().el);
                }, this);
            }
            otherResultsContainer.slideDown();
            this.otherResultShowed = true;
        },

        closeEditor: function(){
            entryCollection.current_editor_index = null;
            this.$el.hide();
        },

        render: function(){
            this.otherResultShowed = false;
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },

        hotKeysHandler: function(e){
            if(e.ctrlKey && e.keyCode == 13){
                this.ctrlEnterKeyInput();
            }
            if(e.ctrlKey && e.keyCode == 38){
                this.ctrlUpKeyInput();
            }
            if(e.ctrlKey && e.keyCode == 40){
                this.ctrlDownKeyInput();
            }
        },

        ctrlEnterKeyInput: function(){
            console.info('If you want to handle the ctrl+enter key event, you just override this Function');
        },

        ctrlUpKeyInput: function(){
            console.info('If you want to handle the ctrl+up key event, you just override this Function');
        },

        ctrlDownKeyInput: function(){
            console.info('If you want to handle the ctrl+down key event, you just override this Function');
        }
    });

    var TranslateEditorView = BaseEditorView.extend({
        template: _.template(require('./templates/translate_input.tpl')),

        className: 'translate-editor',

        extra_events: {
            'click .close-editor': 'closeEditor',
            'click .submit-result': 'addTransResult',
            'click .up-vote': 'upVote',
            'keyup #result-input': 'hotKeysHandler'
        },

        resize: function(options){
            this.$el.show().offset(options.offset).width(options.width);
        },

        ctrlEnterKeyInput: function(){
            this.addTransResult();
            this.nextEntry();
        },

        ctrlDownKeyInput: function(){
            this.nextEntry();
        },

        ctrlUpKeyInput: function(){
            this.preEntry();
        },

        addTransResult: function(){
            var url = url_map.add_trans_result,
                target_text = this.$('#result-input').val();

            if(target_text.trim() === ''){
                alertView.alert({category: 'danger', info: '翻译结果不能为空'});
                return;
            }
            if(target_text.trim() === this.model.get('result')){
                alertView.alert({category: 'info', info: '翻译结果没有任何修改'});
                return;
            }

            $.post(url, {
                task_id: task.id,
                entry_id: this.model.get('entry').id,
                entry_position: this.model.get('entry').position,
                tar_lang: current_tar_lang,
                target_text: target_text
            }, $.proxy(function(res){
                if(res.status === 'ok'){
                    this.nextEntry();
                    this.entryView.model.set('result', res.data);
                    this.model.set('result', res.data);
                }else if(res.info === 'not_login'){
                    login.openLoginModal($.proxy(translateToolHeader.loginCallback, translateToolHeader));
                }else{
                    alertView.alert(res);
                }

            }, this));
        }
    });

    var ApproveEditorView = BaseEditorView.extend({
        template: _.template(require('./templates/approve_input.tpl')),
        className: 'approve-editor',

        extra_events: {
            'click .approve-result': 'approveResult',
            'click .next-entry': 'nextEntry',
            'click .pre-entry': 'preEntry'
        },

        approveResult: function(){
            var result = this.model.get('result');
            if(!result){
                alertView.alert({category: 'danger', info: '没有翻译结果需要确认'});
                return;
            }
            this.doApproveResult(result);
        },

        doApproveResult: function(result){
            if(result.used){
                alertView.alert({category: 'info', info: '改翻译结果已经确认，无需重复操作！'});
                return;
            }
            $.get(
                url_map.approve_result_url,
                {
                    result_id: result.id,
                    entry_id: this.model.get('entry').id,
                    task_id: task.id,
                    tar_lang: current_tar_lang
                },
                $.proxy(function(res){
                    if(res.status === 'ok'){
                        this.entryView.model.set('result', res.data);
                        this.nextEntry();
                    }else{
                        alertView.alert(res);
                    }
                }, this)
            );
        }
    });

    var AddGlossaryView = BaseView.extend({
        el: $("#glossary-editor"),
        template: _.template(require('./templates/glossary_editor.tpl')),

        initialize: function(){
            this.opened = false;
            this.glossaryTableCollection = new GlossaryTableCollection();
            this.glossaryTableCollection.on('reset', this.fillGlossaryTables, this);
        },

        events: {
            'click .recommend-glossary': 'recommendGlossary',
            'click .panel': 'clickPanel',
            'click .close-editor': 'closeEditor',
            'click .collect-glossary': 'collectGlossary',
            'click .recommend-form .submit': 'submitRecommendedGlossary',
            'click .collect-form .submit': 'submitCollectedGlossary'
        },

        clickPanel: function(e){
            e.stopPropagation();
        },

        closeEditor: function(){
            this.hide();
        },

        fillGlossaryTables: function(collection){
            var glossary_table_select = this.$("#glossary_tables").empty(),
                option_tpl = _.template('<option value="<%=id%>"><%=name %></option>');
            collection.each(function(model){
                glossary_table_select.append(option_tpl(model.toJSON()));
            });
            if(collection.length <= 0){
                glossary_table_select.append(option_tpl({
                    id: '',
                    name: '请先创建术语表'
                }));
            }
        },

        recommendGlossary: function(e){
            if(e){
                e.stopPropagation();
            }
            this.$('.ops').hide();
            this.$('.recommend-form').show();
            this.$('.collect-form').hide();
        },

        collectGlossary: function(e){
            e.stopPropagation();
            this.glossaryTableCollection.fetch({reset: true});
            this.$('.ops').hide();
            this.$('.recommend-form').hide();
            this.$('.collect-form').show();
        },

        submitRecommendedGlossary: function(){
            var url = url_map.create_glossary,
                source = this.source,
                target = this.$('.recommend-target').val();

            if(!target){
                alertView.alert({category:'danger', info: '术语翻译结果不能为空'});
                return;
            }

            $.post(url, {
                task_id: task.id,
                source: source,
                target: target,
                tar_lang: current_tar_lang
            }, $.proxy(function(res){
                if(res.status === 'ok'){
                    this.hide();
                    glossaryTableListView.pushGlossary(res.data);
                    entryCollection.openCurrentEditor();
                }
                alertView.alert(res);
            }, this))
        },

        submitCollectedGlossary: function(){
            var url = url_map.collect_glossary_url,
                source = this.source,
                target = this.$('.collect-target').val(),
                glossary_table_id = this.$('#glossary_tables').val();

            if(!target){
                alertView.alert({category:'danger', info: '术语翻译结果不能为空'});
                return;
            }
            if(!glossary_table_id){
                alertView.alert({category:'danger', info: '请选择一个术语表'});
                return;
            }

            $.post(url, {
                source: source,
                target: target,
                glossary_table_id: glossary_table_id,
                src_lang: task.src_lang,
                tar_lang: current_tar_lang
            }, $.proxy(function(res){
                if(res.status === 'ok'){
                    this.hide();
                }
                alertView.alert(res);
            }, this))
        },

        hide: function(){
            if(this.opened){
                this.$el.hide();
                this.trigger_cid = null;
                this.opened = false;
            }
        },

        render: function(){
            this.$el.html(this.template({
                position: this.position,
                source: this.source
            }));
            var self = this;
            zero_client.clip(this.$(".copy-source"));

            zero_client.on( 'load', function(client) {
                client.on( 'datarequested', function(client) {
                    client.setText(self.source);
                } );

                client.on( 'complete', function(client, args) {
                    alertView.alert({info: '成功复制到粘贴板', 'category': 'info'});
                    self.hide();
                } );
            } );
            this.opened = true;

            this.$el.css(this.position).show();
            return this;
        }
    });

    var commentTemplate = _.template(require('./templates/comment.tpl'));
    var CommentListView = BaseView.extend({
        el: $('#sarike-slide-sidebar'),

        events: {
            'click .close-slide': 'closeSlide',
            'click .submit-comment': 'submitComment',
            'click .refresh-comments': 'refreshComments'
        },

        initialize: function(){
            this.width = 515;
            this.comment_container = this.$('.media-list');
            this.commentCollection = new CommentCollection();
            this.commentCollection.on('reset', this.addComments, this);

            this.resize();
            $(window).resize($.proxy(this.resize, this));
            this.emptyCommentsContainer();
        },

        emptyCommentsContainer: function(){
            this.comment_container.empty();
            return this;
        },

        resize: function(){
            this.$('.slide-body').height(this.$el.height() - 76);
        },

        refreshComments: function(){
            this.comment_container.empty();
            this.fetchCommentList();
        },

        submitComment: function(){
            var url = url_map.submit_comment_url,
                comment_editor = this.$('.div-input'),
                comment_content = comment_editor.html();
            $.post(url, {
                task_id: task.id,
                comment_content: comment_content
            }, $.proxy(function(res){
                if(res.status == 'ok'){
                    var comment = $(commentTemplate(res.data)).hide();
                    this.$('.media-list').prepend(comment);
                    comment.fadeIn();
                    comment_editor.empty();
                }else{
                    alertView.alert({
                        category: res.category,
                        info: res.info === 'not_login'? '登录后才能发表评论': res.info
                    });
                }
            }, this));
        },
        closeSlide: function(){
            this.$el.animate({
                right: -this.width
            }, 'fast')
        },

        openSlide: function(){
            this.$el.animate({
                right: 0
            }, 'fast')
        },

        fetchCommentList: function(){
            this.commentCollection.fetch({data: {
                task_id: task.id
            }, reset: true});
        },

        addComments: function(collection){
            collection.each($.proxy(function(model){
                this.comment_container.append(commentTemplate(model.toJSON()));
            }, this));
        }
    });

    var editorView = null,
        glossaryMap = {},
        glossaryEditorView = null;

    var EntryView = BaseView.extend({

        className: 'row',

        template: _.template(require('./templates/entry_row.tpl')),

        initialize: function(){
            this.model.on('change:result change:read_mode', this.render, this);
            this.model.on('open-editor-event', this.openEditor, this);
            this.model.on('highlight-entry-word-event', this.render, this);
        },

        events: {
            'click .row-wrapper': 'clickRow',
            'click .glossary-pop-item': 'useGlossary',
            'mouseup .entry': 'selectEnd'
        },

        useGlossary: function(g_target){
            this.openEditor();
            if(editorView){
                var preVal = editorView.$("#result-input").val();
                editorView.$("#result-input").val(preVal + g_target);
            }
        },

        highlightRow: function(){
            this.$el.addClass('active').siblings('.row').removeClass('active');
        },

        selectEnd: function(e){
            e.stopPropagation();
            var selectString = $.trim(window.getSelection().toString());
            if (selectString.trim() != ""){
                this.openGlossaryEditor(e.pageY, e.pageX, selectString);
            }
        },

        openGlossaryEditor: function(top, left, selectString){
            glossaryEditorView = glossaryEditorView || new AddGlossaryView();
            glossaryEditorView.options({
                source: selectString,
                trigger_cid: this.cid,
                position: {'top': top, 'left': left}
            });
            glossaryEditorView.render();
            return glossaryEditorView;
        },

        clickRow: function(e){
            if(e && glossaryEditorView && this.cid == glossaryEditorView.trigger_cid){
//                e.stopPropagation();
                return false;
            }
            this.openEditor();
            return true;
        },

        openEditor: function(){
            if((editorView && entryCollection.current_editor_index === entryCollection.indexOf(this.model))
                || this.toolType === TOOL_TYPE_READ){
                return;
            }

            var target = this.$('.row-wrapper');
            this.highlightRow();

            if(!user['is_authenticated']){
                login.openLoginModal($.proxy(translateToolHeader.loginCallback, translateToolHeader));
            }

            if(!!editorView){
                editorView.remove();
            }

            if(this.toolType === TOOL_TYPE_TRANSLATE){
                editorView = new TranslateEditorView({
                    model: this.model.clone()
                });
                editorView.options({
                    entryView: this,
                    toolType: this.toolType
                });
                editorView.render().$el.css({
                    width: target.width()/2,
                    display: 'block',
                    right: '-1px',
                    top: '-14px'
                }).find('textarea').css({height: target.height()}).end().insertAfter(target);
            }
            if(this.toolType === TOOL_TYPE_APPROVE){
                editorView = new ApproveEditorView({
                    model: this.model.clone()
                });
                editorView.options({
                    entryView: this,
                    toolType: this.toolType
                });
                target.append(editorView.render().el);
            }
            editorView.$("#result-input").focus();
            entryCollection.current_editor_index = entryCollection.indexOf(this.model);
        },

        setToolType: function(toolType){
            this.toolType = toolType;
            return this;
        },

        initGlossaryPopover: function(){
            var glossary_tags = this.$('.glossary'),
                self = this;
            glossary_tags.each(function(index, glossary_tag){
                var $glossary_tag = $(glossary_tag),
                    g_source = $glossary_tag.data('source'),
                    glossary_list = glossaryMap[g_source],
                    pop_content = $(_.template(require('./templates/glossary_popover.tpl'))({glossary_list: glossary_list}));

                var show_glossary_timer = 0,
                    hide_glossary_timer = 0;

                $glossary_tag
                    .popover({
                        html: true,
                        placement: 'top',
                        container: 'body',
                        trigger: 'manual',
                        title: '<a title="添加新翻译" href="javascript:void(0);" class="add-glossary pull-right"><i class="fa fa-plus"></i></a> 翻译列表',
                        content: pop_content,
                        template: '<div class="popover glossary-popover"><div class="arrow"></div><div class="popover-hover"><h3 class="popover-title"></h3><div class="popover-inner"><div class="popover-content"></div></div></div></div>'
                    })
                    .on('show.bs.popover', function(){
                        pop_content.parent('.glossary-popover').height('auto');
                    })
                    .on('shown.bs.popover', function(){
                        var glossaryPopover = pop_content.parents('.glossary-popover'),
                            initHeight = glossaryPopover.height();
                        glossaryPopover.height(initHeight);
                        glossaryPopover.find('.popover-hover').height(initHeight + 35);
                    })
                    .hover(function(){
                        clearTimeout(hide_glossary_timer);
                        show_glossary_timer = setTimeout(function() {
                            $glossary_tag.popover('show');
                            var glossaryPopover = pop_content.parents('.glossary-popover');
                            glossaryPopover.find('.popover-hover').mouseleave(function(){
                                $glossary_tag.popover('hide');
                            });
                            glossaryPopover.find('.popover-hover').mouseenter(function(){
                                clearTimeout(hide_glossary_timer);
                            });
                            glossaryPopover.find('.add-glossary').click(function(e){
                                e.stopPropagation();
                                self.openGlossaryEditor(e.pageY, e.pageX, g_source).recommendGlossary();
                                $glossary_tag.popover('hide');
                            });
                            pop_content.find('.glossary-pop-item').click(function(){
                                self.useGlossary($(this).text().trim());
                            });
                        },300)
                    }, function() {
                        clearTimeout(show_glossary_timer);
                        hide_glossary_timer = setTimeout(function() {
                            $glossary_tag.popover('hide')
                        },500)
                    });
            });
        },

        render: function(){
            this.$el.html(this.template(_.extend(this.model.toJSON(), {toolType: this.toolType})));
            if(this.toolType === TOOL_TYPE_READ){
                this.$el.addClass('read-mode');
            }
            this.initGlossaryPopover();

            if(editorView){
                // 取消编辑器的引用，使EntryView重新渲染后能后顺利 openCurrentEditor
                editorView.remove();
                editorView = null;
            }
            return this;
        }
    });

    var GlossaryItemView = BaseView.extend({
        tagName: 'tr',
        template: _.template(require('./templates/glossary_table_item.tpl')),

        render: function(){
            this.$el.html(this.template(_.extend(this.model.toJSON(), {current_user: user})));
            trigger.addUserInfoPopOverTrigger(this.$('.user-info-pop'));
            return this;
        }
    });

    var IntroView = BaseView.extend({

        template: _.template(require('./templates/intro.tpl')),
        el: $('#intro'),

        events: {
            'click .i-know': 'close'
        },

        initialize: function(){
            this.$el.hide();
        },

        render: function(){
            this.$el.html(this.template());
            return this;
        },

        show: function(){
            this.$el.show();
            $(window).off('keyup').on('keyup', $.proxy(function(e){
                if(e.keyCode === 27){
                    this.close();
                }
            }, this));
            this.$('.intro-pop').show();
            // 禁用滚动条
            $('body').css('overflow', 'hidden');
            // 突出显示主题内容
            $('#glossary-table, #ts').css({
                position: 'relative',
                'z-index': 99999
            });

            $('.i-know').click($.proxy(function(){
                this.close();
            }, this));

            // 突出显示工具栏
            $('.ts-tool-panel').css({
                'z-index': 99999
            });
            cookie.setCookie('intro_showed', true);
        },

        close: function(){
            translateToolControlsBar.$('.tool-group>li a').tooltip('hide');
            $('body').css('overflow', 'auto');
            $('#glossary-table, #ts').css({
                position: 'static',
                'z-index': 'auto'
            });
            // 突出显示工具栏
            $('.ts-tool-panel').css({
                'z-index': 'auto'
            });
            this.$el.fadeOut('fast');
        }
    });

    var TranslateToolAsideControlsView = BaseView.extend({
        template: _.template(require('./templates/aside_controls_bar.tpl')),

        el: $('#ts-aside-controls'),

        events: {
            'click .open-glossary-table': 'openGlossaryTable',
            'click .tool-group>li': 'activeTab',
            'click .refresh': 'refreshTransTool',
            'click .change-mode': 'changeReadMode',
            'click .toggle-ts-tool-bar': 'toggleTsToolBar',
            'click .toggle-task-image-slide': 'toggleTaskImageSlide',
            'click .to-translate': 'startTranslate',
            'click .preview': 'preView',
            'click .show-intro': 'showIntro',
            'click .slide-left': 'slideLeft',
            'click .slide-right': 'slideRight',
            'click .open-comments': 'openCommentList'
        },

        slideLeft: function() {
            var slideContent = this.$('.task-image-slide-inner'),
                curTop = parseInt(slideContent.css('left')) || 0,
                newTop = curTop + 178;
            slideContent.css('left', newTop);
            if(newTop > 0){
                setTimeout(function(){
                    slideContent.css('left', 0);
                }, 200);
            }
        },

        slideRight: function() {
            var slideContent = this.$('.task-image-slide-inner'),
                curTop = parseInt(slideContent.css('left')) || 0,
                newTop = curTop - 178;
            slideContent.css('left', newTop);
            if((Math.abs(newTop) + 178) - slideContent.width() >= 178){
                setTimeout(function(){
                    slideContent.css('left', curTop);
                }, 200);
            }
        },

        toggleTsToolBar: function(){
            this.$('.ts-tool-bar').toggleClass('opened');
        },

        toggleTaskImageSlide: function(){
            var slide = this.$('.task-image-slide');
            slide.toggleClass('opened');
        },

        showIntro: function(){
            introView.show();
        },

        closeGlossaryTable: function(){
            translateTool.$el.show();
            glossaryTableListView.$el.hide();
        },

        openGlossaryTable: function(){
            translateTool.$el.hide();
            glossaryTableListView.$el.show();
        },

        openCommentList: function(){
            commentListView.openSlide();
        },

        activeTab: function(e){
            var target = $(e.currentTarget);
            if(target.hasClass('no-tab')){
                return;
            }
            $(e.currentTarget).addClass('active').siblings('li').removeClass('active');
        },

        startTranslate: function(e){
            e.preventDefault();
            this.closeGlossaryTable();
            router.navigate(TOOL_TYPE_TRANSLATE + '/' + current_tar_lang, {trigger: true, replace: true});
        },

        preView: function(read_mode){
            router.navigate(TOOL_TYPE_READ + '/' + current_tar_lang + '/' + read_mode, {trigger: true});
        },

        changeReadMode: function(e){
            this.closeGlossaryTable();
            var $target = $(e.currentTarget),
                read_mode = $target.data('mode') || READ_MODE_ORIGIN;
//            this.$('.current-mode').text($target.text());
            if(translateTool.toolType !== TOOL_TYPE_READ){
                this.preView(read_mode);
            }else{
                entryCollection.each(function(model){
                    model.set('read_mode', read_mode);
                });
            }
        },

        initLanguageList: function(){
            this.$('.current-language').text('[' + current_tar_lang.toUpperCase() + ']' + supported_languages[current_tar_lang]);

            var language_list_tpl = '<li><a href="#<%=toolType %>/<%=tar_lang %>"><%=pretty_lang%></a></li>';

            this.$('.language-list').empty();

            var tar_lang_list = task['tar_lang_list'];
            if(tar_lang_list.length === 0){
                this.$('.language-list').remove();
            }else{
                _.each(tar_lang_list, $.proxy(function(tar_lang){
                    this.$('.language-list').append(_.template(language_list_tpl)({
                        tar_lang: tar_lang,
                        toolType: translateTool.toolType,
                        pretty_lang: '[' + tar_lang.toUpperCase() + ']' + supported_languages[tar_lang]
                    }))
                }, this));
            }
        },

        refreshTransTool: function(e){
            e.stopPropagation();
            translateTool.refresh(e);
        },

        render: function(){
            this.$(".ts-tool-bar").html(this.template({
                toolType: translateTool.toolType,
                user: user
            })).html();
            this.initLanguageList();
            this.$('.tool-group>li a').tooltip('destroy').tooltip({
                placement: 'right',
                container: 'body'
            });
            return this;
        }
    });

    var GlossaryListView = BaseView.extend({

        el: $('#glossary-table'),

        initialize: function(){
            this.$el.hide();
            this.glossaryCollection = new GlossaryCollection();
            this.glossaryCollection.on('reset', this.glossaryReady, this);
            this.glossaryCollection.on('add', this.newGlossaryAdded, this);
        },

        newGlossaryAdded: function(model){
            var g_source = model.get('source');
            if(glossaryMap[g_source]){
                glossaryMap[g_source].push(model.toJSON());
            }else{
                glossaryMap[g_source] = [model.toJSON()];
            }
            this.highlightGlossary();
        },

        pushGlossary: function(glossary){
            this.glossaryCollection.add(glossary);
        },

        glossaryReady: function(collection){
            glossaryMap = {};
            collection.each(function(glossary){
                var source = glossary.get('source'),
                    target = glossary.get('target');
                if(glossaryMap[source]){
                    glossaryMap[source].push(glossary.toJSON());
                }else{
                    glossaryMap[source] = [glossary.toJSON()];
                }
            }, this);

            this.highlightGlossary();
            this.addGlossaries();
        },

        highlightGlossary: function(){
            entryCollection.each(function(entry_model){
                var entry = entry_model.get('entry'),
                    entry_word = entry['word'],
                    highlighted_word = entry_word,
                    contained_glossaries = [];

                _.each(glossaryMap, function(glossary_list, glossary_source){
                    var reg = new RegExp(glossary_source, 'g');
                    if(reg.test(entry_word)){
                        contained_glossaries.push(glossary_list[0]);
                    }
                }, this);

                var sorted_glossary = _.sortBy(contained_glossaries, function(g){return g.source.length});

                _.each(sorted_glossary, function(glossary){
                    var reg = new RegExp('(' + glossary.source + ')', 'g');
                    if(reg.test(highlighted_word)){
                        highlighted_word = highlighted_word.replace(reg, function($1){
                            return _.template(require('./templates/glossary_replacement.tpl'))({
                                source: $1
//                                glossary_list: glossaryMap[$1]
                            })
                        })
                    }
                });
                if(highlighted_word != entry_word){
                    entry.highlighted_word = highlighted_word;
                    entry_model.set('entry', entry);
                    entry_model.trigger('highlight-entry-word-event');
                }
            }, this);
        },

        addGlossaries: function(){
            this.$('.glossary-list').empty();
            _.each(glossaryMap, function(glossary_list, source){
                this.addGlossary(new Backbone.Model({
                    glossary_list: glossary_list,
                    source: source
                }))
            }, this);
        },

        addGlossary: function(model){
            var glossaryItem = new GlossaryItemView({
                model: model
            });
            this.$('.glossary-list').append(glossaryItem.render().el);
        },

        fetchGlossaries: function(){
            this.glossaryCollection.fetch({
                data:{
                    task_id: task.id
                },
                success: function(){
                    entryCollection.openCurrentEditor();
                },
                reset: true
            })
        },

        render: function(){
            this.fetchGlossaries();
            return this;
        }
    });

    var TranslateToolHeaderView = BaseView.extend({
        el: $('.ts-header'),

        template: _.template(require('./templates/header.tpl')),

        events: {
            'click .login-btn': 'openLogin',
            'click .register-btn': 'openRegister',
            'click .logout-btn': 'logout'
        },

        loginCallback: function(data){
            user = data;
            this.render();
        },

        openLogin: function(){
            login.openLoginModal($.proxy(this.loginCallback, this));
        },

        openRegister: function(){
            login.openRegisterModal();
        },

        logout: function(e){
            login.logout($.proxy(function(){
                user.is_authenticated = false;
                user.nickname = '';
                this.render();
            }, this));
        },

        render: function(){
            this.$el.html(this.template(user));
            return this;
        }
    });

    var TranslateToolView = BaseView.extend({

        el: $('#ts'),

        events: {
            'click #scroll-top': 'scrollToTop'
        },

        initialize: function(){
            this.$("#entry-list").empty();
            entryCollection.on("reset", this.addEntries, this);
        },

        addEntries: function(collection){
            if(collection.length > 0){
                collection.each(this.addEntry, this);
            }

            entryCollection.openCurrentEditor();

            // 词条加载完成后在加载术语
            glossaryTableListView.render();
        },

        addEntry: function(entry){
            var entryView = new EntryView({
                model: entry
            });
            this.$("#entry-list").append(entryView.setToolType(this.toolType).render().el);
        },

        renderCompleteView: function(){
            var complete_view_template = _.template(require('./templates/translate_complete.tpl'));
            this.$("#entry-list").html(complete_view_template());
        },

        fetchEntries: function(){
            entryCollection.fetch({
                data: {
                    task_id: task.id,
                    tar_lang: current_tar_lang
                },
                reset: true
            });
        },

        render: function(){
            if(this.toolType == TOOL_TYPE_TRANSLATE && is_completed(current_tar_lang)){
                this.renderCompleteView();
            }else{
                this.fetchEntries();
            }
            return this;
        },

        refresh: function(e){
            e.preventDefault();
            this.$("#entry-list").empty();
            this.fetchEntries();
        }
    });

    /* -------------------image trans--------------------- */
    var ImageModel = Backbone.Model.extend({
        defaults: {
            imgUrl: undefined,
            position: undefined
        }
    });

    var ImageCollection = Backbone.Collection.extend({
        url: "/translate/fetch_images",
        model: ImageModel,

        parse: function(res) {
            if(res.info == 'ok') {
                return res.data;
            }
        }
    });

    var ImgTransToolView = Backbone.View.extend({
        el: $('#ts'),

        initialize: function() {
            this.listenTo(this.collection ,"reset", this.addImages);
        },

        addImages: function() {
            if(this.collection.length > 0){
                this.collection.each(this.addOneImage, this);
            }

            // 词条加载完成后在加载术语
//            glossaryTableListView.render();
        },

        addOneImage: function(image) {

        },

        render: function() {
            this.collection.each(function(image) {
            });
        }
    });
    /* -------------------------------------------------- */



    var entryCollection = null,
        translateTool = null,
        translateToolHeader = null,
        translateToolControlsBar = null,
        commentListView = null,
        introView = null,
        glossaryTableListView = null;

    var NowDoRouter = Backbone.Router.extend({

        routes: {
            "": "openTranslateTool",
            ":tool_type": "openTranslateTool",
            ":tool_type/:tar_lang": "openTranslateTool",
            "read/:tar_lang/:read_mode": "openReadTool"
        },

        openReadTool: function(tar_lang, read_mode){
            this.openTranslateTool(TOOL_TYPE_READ, tar_lang, read_mode);
        },

        openTranslateTool: function(tool_type, tar_lang, read_mode){
            if(task.type === 0){
                current_tar_lang = tar_lang || task['tar_lang_list'][0];
                current_read_mode = read_mode || READ_MODE_ORIGIN;
                //词条列表
                entryCollection = new EntryCollection();

                //工具主体（翻译工具，阅读工具，确认工具）
                translateTool = new TranslateToolView().options({
                    toolType: tool_type || TOOL_TYPE_TRANSLATE
                }).render();

                //右侧边工具栏
                translateToolControlsBar = translateToolControlsBar || new TranslateToolAsideControlsView().render();
                // 顶栏
                translateToolHeader = translateToolHeader || new TranslateToolHeaderView().render();
                // 帮助
                introView = introView || new IntroView().render();
                if(!cookie.getCookie('intro_showed')){
                    introView.show();
                }
                //术语表(会在词条渲染完成以后渲染到词条中去)
                glossaryTableListView = glossaryTableListView || new GlossaryListView();
                commentListView = commentListView || new CommentListView();
                commentListView.emptyCommentsContainer().fetchCommentList();
            } else if(task.type === 1) {
                current_tar_lang = tar_lang || task['tar_lang_list'][0];

                var imgCollection = new ImageCollection();
                var imgTransTool = new ImgTransToolView({
                    collection: imgCollection
                }).render();
            }
        }
    });

    exports.init = function(task_obj, supported_languages_map, current_user){
        task = task_obj;
        supported_languages = supported_languages_map;
        user = current_user;

        $(window).off('click').click(function(){
            if(glossaryEditorView){
                glossaryEditorView.hide();
            }
        });

        router = new NowDoRouter();
        Backbone.history.start();
    };
});