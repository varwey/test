<td>
    <%=source %>
</td>
<td>
    <ul class="list-unstyled">
        <% _.each(glossary_list, function(glossary){ %>
            <li>
                <%=glossary.target %>
                <span class="meta pull-right">
                    <a href="javascript:void(0);" class="<% if(current_user.id != glossary.creator_id){ %>user-info-pop<% } %>" data-user_id="<%=glossary.creator_id %>">
                        <%=glossary.creator_nickname %>
                    </a>
                    创建于 <%=glossary.created_date %>
                </span>
            </li>
        <% })%>
    </ul>
</td>