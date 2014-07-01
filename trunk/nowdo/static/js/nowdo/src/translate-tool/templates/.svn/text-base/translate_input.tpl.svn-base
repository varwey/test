<div class="panel panel-xc">
    <div class="panel-body">
        <textarea name="" class="form-control" id="result-input" cols="30" rows="5"><%= result?result.content:'' %></textarea>
    </div>

    <div class="panel-footer clearfix">
        <button class="btn btn-primary submit-result btn-sm">提交</button>
        <button class="btn btn-default close-editor btn-sm">取消</button>
                <span class="creator-info">
                    <% if(result){ %>
                        由 <%=result.translator %> 更新于 <%=result.modified_date_delta %>
                    <% }else{ %>
                        暂时还没有翻译结果
                    <% } %>
                </span>
        <div class='pull-right'>
            <a href="javascript:void(0);" class="show-other-results">更多结果
                <i class="fa fa-angle-double-down"></i>
            </a>
        </div>
    </div>
    <ul class="other-results" style="display:none;">

    </ul>
</div>