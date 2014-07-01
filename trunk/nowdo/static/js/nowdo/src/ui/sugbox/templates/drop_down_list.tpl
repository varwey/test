    <li><a href="/tag?tag=<%= search_name %>"><i class="fa fa-tag"></i>进入 <span><%= hl(search_name, search_name) %></span> 标签 ></a></li>
    <% _.each(tag_results, function(tag){ %>
    <li><a href="/tag?tag=<%= tag.tag_name %>" title="<%= tag.tag_name %>"><span><%= hl(search_name, tag.tag_name) %></span></a></li>
    <% }) %>
    <li class="divider"></li>
    <li><a href="#"><i class="fa fa-user"></i><span><%= hl(search_name, search_name) %></span> 相关的主题</a></li>
    <% _.each(task_results, function(task){ %>
    <li><a href="/task/view/<%= task.id %>" title="<%= task.name %>"><span><%= hl(search_name, task.name) %></span></a></li>
    <% }) %>