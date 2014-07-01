    <input class="form-control" id="img_name" name="img_name" placeholder="标题" type="text" value="">
    <div class="">
    <div id="files" class="files"></div>
    <div id="progress" class="progress hide">
        <div class="progress-bar progress-bar-success"></div>
    </div>
    <div class="dropzone">
        <div class="dropzone-info">
        </div>
        <input id="fileupload" type="file" name="file" accept="image/gif, image/jpeg, image/png">
    </div>
    <input class="form-control" id="img-tags" placeholder="标签，多个标签用逗号分隔" type="text" value="" style="border-top: 1px dashed #eee;">
    </div>
    <div class="panel-footer">
        <label class="checkbox-inline">
            <input checked="checked" id="status" name="status" type="checkbox"> 我要翻译这些图片
        </label>

        <div class="language-select" style="display: inline-block;">
            <select name="src_lang">
                <% _.each(_.keys(supported_languages), function(language) { %>
                <% if(language === src_lang) { %>
                <option selected="selected" value="<%= language %>"><%= supported_languages[language] %></option>
                <% } else { %>
                <option value="<%= language %>"><%= supported_languages[language] %></option>
                <% } %>
                <% }) %>
            </select>
            <i class="fa fa-random"></i>
            <select name="tar_lang">
                <% _.each(_.keys(supported_languages), function(language) { %>
                <% if(language === tar_lang) { %>
                <option selected="selected" value="<%= language %>"><%= supported_languages[language] %></option>
                <% } else { %>
                <option value="<%= language %>"><%= supported_languages[language] %></option>
                <% } %>
                <% }) %>
            </select>
        </div>

        <a class="btn img-publish pull-right" data-loading-text="正在发布...">发布</a>
        <a class="btn img-preview pull-right" href="javascript:void(0);">预览</a>
        <a class="btn close-editor pull-right" href="javascript:void(0);">取消</a>
    </div>
