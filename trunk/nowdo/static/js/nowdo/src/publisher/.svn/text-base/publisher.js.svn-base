/**
 * Created by SL on 14-4-29.
 */

define(function (require, exports, module) {
    require('jquery-form');
    require('fileupload');

    var Backbone = require('backbone'),
        _ = require('underscore'),
        alert = require('../ui/alert/alert'),
        html = require('../utils/html'),
        confirm = require('../ui/confirm/confirm'),
        $ = require('$');

    var imgUploaderTemplate = require("./templates/img_uploader.tpl");
    var smallDropzoneTemplate = require("./templates/small_dropzone.tpl");
    var bigDropzoneTemplate = require("./templates/big_dropzone.tpl");
    var imgItemTemplate = require("./templates/img_item.tpl");

    var BaseEditor = Backbone.View.extend({

    });

    var TextEditor = BaseEditor.extend({
        editor_name: 'text_editor',

        events: {
            'change #status': 'toggleTranslate',
            'submit form': 'onSubmit',
            'click .task-preview': 'taskPreview'
        },

        toggleTranslate: function (e) {


            var opened = $(e.currentTarget).prop('checked');
            if (opened) {
                this.$('.language-select').css('display', 'inline-block');
//                confirm.activeTranslationConfirm()
//                    .onOk($.proxy(function(){
//                        this.$('.language-select').css('display', 'inline-block');
//                        var pre_code = this.$('#task_content').code();
//                        this.$('#task_content').destroy().val(html.strip_tags(pre_code));
//                    }, this))
//                    .onCancel($.proxy(function(){
//                        this.$('.language-select').css('display', 'none');
//                        $(e.currentTarget).prop('checked', false);
//                    }, this));
            } else {
                this.$('.language-select').css('display', 'none');
//                var pre_code = this.$('#task_content').val();
//                this.initSummerNote().code(pre_code.replace(/\n/g, '<br/>'));
            }
        },

        sendFile: function (file, editor, welEditable) {
            var data = new FormData();
            data.append("file", file);
            $.ajax({
                data: data,
                type: "POST",
                url: "/file/save",
                cache: false,
                contentType: false,
                processData: false,
                success: function (res) {
                    if (res.status == 'ok') {
                        editor.insertImage(welEditable, res.url);
                    } else {
                        alert.alert(res);
                    }
                }
            });
        },

        taskPreview: function () {
            var task_name = this.$('form #task_name').fieldValue()[0],
//                task_content = this.$('form #task_content').fieldValue()[0],
                task_content = this.$('#task_content').code(),
                tags = this.$('form #tags').fieldValue()[0],
                status = this.$('form #status').prop('checked');

            var preview_form = $(_.template(require('./templates/preview_form.tpl'))({
                task_name: task_name,
                task_content: task_content,
                status: status,
                tags: tags
            }));

            if (this.validateForm(preview_form)) {
                preview_form.submit();
            }
        },

        initSummerNote: function () {
            return this.$('#task_content').summernote({
                height: "300px",
                lang: 'zh-CN',
                toolbar: [
                    ['insert', ['picture', 'link']]
                ],
                onImageUpload: $.proxy(function (files, editor, welEditable) {
                    var target_file = files[0];
                    if (!target_file) {
                        return;
                    }
                    if (!(/\.(gif|jpg|jpeg|png)$/i).test(target_file.name)) {
                        alert.alert({info: '不支持的图片格式', category: 'danger'});
                        return;
                    }
                    if (target_file.size > 3 * 1024 * 1024) {
                        alert.alert({info: '文件最大不能超过3M', category: 'danger'});
                        return;
                    }
                    this.sendFile(files[0], editor, welEditable);
                }, this),
                onpaste: function (e) {
                    var textType = 'text/html';
                    var html;
                    if (window.clipboardData) {
                        html = window.clipboardData.getData(textType);
                    } else {
                        var clipboard = e.originalEvent.clipboardData;
                        if (clipboard && _.indexOf(clipboard.types, textType) >= 0) {
                            html = clipboard.getData(textType)
                        }
                    }

                    if (!html) {
                        //如果没有读取到html，则进行默认操作
                        return
                    }

                    e.preventDefault()

                    function resetAttributes(node) {
                        var tag = $(node);
                        var attributes = $.map(tag[0].attributes || [], function (item) {
                            return item.nodeName;
                        });

                        for (var i = 0; i < attributes.length; i++) {
                            var item = attributes[i];
                            if (item != 'href' && item != 'src') {
                                tag.removeAttr(item);
                            }
                        }
                        if (tag.get(0).tagName === 'A') {
                            tag.attr('target', '_blank')
                        }
                    }

                    html = html.replace(/<(?!(p|\/p|a|\/a|br|img)).*?>/ig, '');

                    var sel, range;
                    sel = window.getSelection();
                    if (sel.getRangeAt && sel.rangeCount) {
                        range = sel.getRangeAt(0);
                        range.deleteContents();
                        // Range.createContextualFragment() would be useful here but is
                        // non-standard and not supported in all browsers (IE9, for one)
                        var el = document.createElement("div");
                        var frag = document.createDocumentFragment(), node, lastNode;
                        if (html) {
                            el.innerHTML = html;
                            while ((node = el.firstChild)) {
                                //remove attribute
                                var tag = $(node);
                                var elems = tag.find('*')
                                resetAttributes(node)
                                if (tag.get(0).tagName === 'A') {
                                    if (!tag.html() || !tag.html().trim()) {
                                        tag.remove();
                                        continue;
                                    }
                                }

                                for (var i = 0; i < elems.length; i++) {
                                    resetAttributes(elems[i]);
                                    if (tag.get(0).tagName === 'A') {
                                        if (!tag.html() || !tag.html().trim()) {
                                            tag.remove();
                                            continue;
                                        }
                                    }
                                }

                                lastNode = frag.appendChild(node);
                            }
                        }
                        range.insertNode(frag);
                        // Preserve the selection
                        if (lastNode) {
                            range = range.cloneRange();
                            range.setStartAfter(lastNode);
                            range.collapse(true);
                            sel.removeAllRanges();
                            sel.addRange(range);
                        }
                    }
                }
            });
        },

        validateForm: function ($form) {
            if (!$form.find('#task_name').val()) {
                alert.alert({
                    info: '标题不能为空',
                    category: 'danger'
                });
                return false;
            }
            if (!$form.find('#task_content').val()) {
                alert.alert({
                    info: '主题内容不能为空',
                    category: 'danger'
                });
                return false;
            }
            if (!$form.find('#tags').val()) {
                alert.alert({
                    info: '标签不能为空',
                    category: 'danger'
                });
                return false;
            }
            return true;
        },

        onSubmit: function (e) {
            e.preventDefault();
            $(e.currentTarget).ajaxSubmit({
                beforeSubmit: $.proxy(function (form_data, $form, options) {
                    if (this.validateForm($form)) {
                        this.$('.btn[type=submit]').button('loading');
                        return true;
                    }
                    return false;
                }, this),
                success: $.proxy(function () {
                    if (this.redirect) {
                        location.href = this.redirect;
                    } else {
                        location.reload();
                    }
                }, this),
                complete: $.proxy(function () {
                    this.$('.btn[type=submit]').button('reset');
                }, this)
            });
            return false;
        },

        render: function () {
            this.initSummerNote();
            return this;
        }
    });

    var LangModel = Backbone.Model.extend({
        url: '/nowdo_languages',

        defaults: {

        },

        parse: function(res) {
            if(res.status === 'ok') {
                return res.data;
            }
        }
    });

    var ImageModel = Backbone.Model.extend({
        defaults: {
            imgUrl: undefined
        }
    });

    var ImageCollection = Backbone.Collection.extend({
        model: ImageModel,

        moveToIndex: function (model, index) {
            if (index > 0) {
                this.remove(model, {silent: true}); // silence this to stop excess event triggers
                this.add(model, {at: index - 1});
            }
        }
    });

    var ImageUpload = Backbone.View.extend({
        template: _.template(imgUploaderTemplate),

        events: {
            "change #status": 'toggleTranslate',
            "click .operatebar": "removeImg",
            "click .img-preview": "imgPreview",
            "click .img-publish": "imgPublish"
        },

        initialize: function () {
            this.langModel = new LangModel;
            this.imgCount = 0;
//            this.collection = new ImageCollection;
            this.listenTo(this.langModel, 'change', this.render);
            this.langModel.fetch();
        },

        render: function () {
            this.$el.html(this.template({
                supported_languages: this.langModel.get('supported_languages'),
                src_lang: 'cn',
                tar_lang: 'en'
            }));
            this.$('.dropzone-info').html(_.template(bigDropzoneTemplate));
            this.initUploader();
            return this;
        },

        toggleTranslate: function (e) {
            var opened = $(e.currentTarget).prop('checked');
            if (opened) {
                this.$('.language-select').css('display', 'inline-block');
            } else {
                this.$('.language-select').css('display', 'none');
            }
        },

        imgPreview: function(e) {
            e.preventDefault();
        },

        imgPublish: function(e) {
            e.preventDefault();
            var url = "/task/create_img_task"

            var task_name = this.$("#img_name").val();
            var img_tags = this.$("#img-tags").val();

            if(!task_name || !task_name.trim()){
                alert.alert({
                    info: '标题不能为空',
                    category: 'danger'
                });
                return false;
            }

            if(!img_tags || !img_tags.trim()){
                alert.alert({
                    info: '标签不能为空',
                    category: 'danger'
                });
                return false;
            }

            var imgElemList = this.$("#files").find('img');

            if(!imgElemList.length) {
                alert.alert({
                    info: '图片不能为空',
                    category: 'danger'
                });
                return false;
            }

            var imgList = [];
            _.each(imgElemList, function(imgElem) {
                imgList.push($(imgElem).attr('src'));
            });

            var src_lang = this.$('select[name="src_lang"]').val();
            var tar_lang = this.$('select[name="tar_lang"]').val();

            var data = {
                task_name: task_name.trim(),
                tags: img_tags,
                img_list: imgList,
                src_lang: src_lang,
                tar_lang: tar_lang
            };

            $.ajax({
                url: url,
                data: data,
                dataType: "json",
                method: "post",
                success: function(res) {
                    if(res.status === 'ok') {
                        location.reload();
                    }
                },
                error: function(xhr, status, error) {
                    console.log(error)
                }
            })
        },

        removeImg: function(e) {
            var $elem = $(e.target);
            var $tmp = $elem.parent();
            if($tmp && $tmp.hasClass('img-wrap')){
                $tmp.remove();
            } else {
                $tmp = $tmp.parent();
                if($tmp && $tmp.hasClass('img-wrap')){
                    $tmp.remove();
                }
            }
            this.imgCount -= 1;
            if(this.imgCount === 0) {
                this.$('.dropzone-info').removeClass("dropzone-info-small");
                this.$('.dropzone-info').html(_.template(bigDropzoneTemplate));
            } else if(this.imgCount == 11){
                this.$('.dropzone').show();
            }
        },

        initUploader: function () {
            var url = "/file/save";
            $('#fileupload').fileupload({
                dropZone: $('.img-uploader'),
                url: url,
                dataType: 'json',
                done: $.proxy(function (e, data) {
//                    this.collection.create({
//                      imgUrl: data.result.url
//                    })
                    this.$('#' + data.files[0].id).find('.img-uploding').hide();
                    this.$('#' + data.files[0].id).find('img').attr('src', data.result.url).show();

                    this.imgCount += 1;
                    if (this.imgCount) {
                        this.$('.dropzone-info').addClass("dropzone-info-small");
                        this.$('.dropzone-info').html(_.template(smallDropzoneTemplate));
                    }
                    if (this.imgCount == 12) {
                        this.$('.dropzone').hide();
                    }
                    $(".img-wrap").hover(
                        function () {
                            $(this).find(".operatebar").removeClass("hide");
                        }, function () {
                            $(this).find(".operatebar").addClass("hide");
                        }
                    );
                }, this),
                progress: $.proxy(function(e, data) {
                    var progress = parseInt(data.loaded / data.total * 100, 10);
                    if(progress === 100) {
                        progress = 99;
                    }
                    this.$('#' + data.files[0].id).find(".upload-no").html(progress + "%");
                }, this),
                send: function(e, data) {
                    var file = data.files[0];
                    if (!(/\.(gif|jpg|jpeg|png)$/i).test(file.name)) {
                        alert.alert({info: '不支持的图片格式', category: 'danger'});
                        return false;
                    }
                    if (file.size > 3 * 1024 * 1024) {
                        alert.alert({info: '文件最大不能超过3M', category: 'danger'});
                        return false;
                    }

                    data.files[0].id = (new Date()).valueOf();
                    $("#files").append(_.template(imgItemTemplate)({
                        id: data.files[0].id
                    }));
                }
            });

            $(document).bind('drop', function (e) {
                e.preventDefault();
            });

            $(document).bind('dragover', $.proxy(function (e) {
                e.preventDefault();
                var dropZone = this.$('.dropzone');

                var timeout = this.dropZoneTimeout;
                if (!timeout) {
                    dropZone.addClass("dropzone-hover");
                    this.$(".dropzone-text-hover").removeClass("hide");
                    this.$(".dropzone-text-normal").addClass("hide")
                } else {
                    clearTimeout(timeout);
                }

//                var found = false,
//                    node = e.target;
//                do {
//                    if (node === dropZone[0]) {
//                        found = true;
//                        break;
//                    }
//                    node = node.parentNode;
//                } while (node != null);
//                if (found) {
//                    dropZone.addClass("dropzone-hover");
//                    this.$(".dropzone-text-hover").removeClass("hide");
//                    this.$(".dropzone-text-normal").addClass("hide")
//                } else {
//                    dropZone.removeClass("dropzone-hover");
//                    this.$(".dropzone-text-hover").addClass("hide");
//                    this.$(".dropzone-text-normal").removeClass("hide")
//                }

                this.dropZoneTimeout = setTimeout($.proxy(function () {
                    this.dropZoneTimeout = null;
                    dropZone.removeClass("dropzone-hover");
                    this.$(".dropzone-text-hover").addClass("hide");
                    this.$(".dropzone-text-normal").removeClass("hide")
                }, this), 100);
            }, this));

            var movElem = null;

            this.$("#files").sortable({
                helper: "clone",
                tolerance: "pointer",
                placeholder: {
                    element: function (currentItem) {
                        return $('<span class="sortable-placeholder"><span class="placeholder-divider"></span></span>')[0];
                    },
                    update: function (container, p) {
                        return;
                    }
                },
                start: function (event, ui) {
                    movElem = $('#files').find('div:hidden');
                    movElem.show().addClass("opacity-half");
                },
                stop: function (event, ui) {
                    movElem.removeClass("opacity-half");
                }
            });
        }
    });

    var ComingView = BaseEditor.extend({
        editor_name: 'coming_editor'
    });

    exports.PublisherView = Backbone.View.extend({
        el: $('.panel-publisher'),

        events: {
            'click .publisher-btn': 'openEditor',
            'click .close-editor': 'closeEditor'
        },

        options: function (options) {
            _.extend(this, options);
            return this;
        },

        initialize: function () {
            this.redirect = null;
            this.text_editor = null;
            this.editors = {};
        },

        openEditor: function (e) {
            var data_target = $(e.currentTarget).data('target');
            switch (data_target) {
                case 'text':
                    this.toggleTextEditor();
                    break;
                case 'image':
                    this.toggleImageUploader();
                    break;
                default :
                    this.toggleEmpty(data_target);
            }
        },

        toggleEditor: function(elem, editor) {
            if(elem.$el.is(":hidden")){
                _.each(_.keys(this.editors), function(key){
                    if(key != editor){
                        this.close(this.editors[key]);
                    }
                }, this);
                elem.$el.slideDown('fast');
            } else {
                elem.$el.slideUp('fast');
            }

        },

        toggleTextEditor: function () {
            if(!this.editors.text_editor) {
                var editor = new TextEditor({
                    el: this.$('.text-editor')
                }).render();
                this.editors.text_editor = editor;
            }

            this.toggleEditor(this.editors.text_editor, 'text_editor');
            this.editors.text_editor.$('#task_name').focus();
        },

        toggleImageUploader: function () {
            if(!this.editors.image_uploader) {
                var editor = new ImageUpload({
                    el: this.$('.img-uploader')
                });
                this.editors.image_uploader = editor;
            }

            this.toggleEditor(this.editors.image_uploader, 'image_uploader');
            this.editors.image_uploader.$('#img_name').focus();
        },

        toggleEmpty: function (data_target) {
            if(!this.editors.empty_editor) {
                var editor = new ComingView({
                    el: this.$('.coming')
                });
                this.editors.empty_editor = editor;
            }

            this.toggleEditor(this.editors.empty_editor, 'empty_editor');
        },

        toggle: function (element, callback, speed) {
            if (element) {
                if(element.$el.is(":hidden")){
                     element.$el.slideDown(speed || 'fast', callback);
                } else {
                    element.$el.slideDown(speed || 'fast', callback);
                }
            } else if (typeof callback === 'function') {
                callback.call()
            }
        },

        closeEditor: function () {
            this.close(this.editor);
        },

        closeUploader: function () {
            this.close(this.uploader);
        },

        close: function (element) {
            element.$el.hide();
            delete element;
        }
    });
});
