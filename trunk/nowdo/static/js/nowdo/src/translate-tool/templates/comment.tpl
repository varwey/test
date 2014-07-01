<li class="media media-comment">
    <a class="pull-left" href="<%=creator_home_url %>">
        <img class="media-object" src="<%=avatar_url %>" alt="<%=nickname %>">
    </a>
    <div class="media-body">
        <div class="media-heading">
            <a href="<%=creator_home_url %>" class="author-link">
                <%=nickname %>
            </a>
                    <span class="pull-right">
                        <%=create_date_delta %>
                    </span>
        </div>
        <%=comment_content %>
    </div>
</li>