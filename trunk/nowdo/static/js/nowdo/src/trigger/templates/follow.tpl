<a class="follow" href="javascript: void(0);" title="关注此人"
   data-user_id="<%=user_id %>"
    <% if(iconOnly){ %>
        data-icon-only="<%=iconOnly %>"
    <% } %>
    <% if(iconStyle){ %>
        data-icon-style="<%=iconStyle %>"
    <% } %>
    data-loading-text="<%=loadingText|| '正在提交...' %>">
    <i class="fa fa-plus<%= iconStyle? '-' + iconStyle : '' %>"></i> <% if(!iconOnly){ %>关注<% } %>
</a>