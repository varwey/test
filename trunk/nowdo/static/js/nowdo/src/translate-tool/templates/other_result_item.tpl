<div class="other-result-content">
    <div class="result-heading">
        <a href="javascript:void(0);" class="user-info-pop" data-email="<%=email %>">
            <strong>
                <%= translator %>
            </strong>
        </a>
        <span class="meta">
            <%= modified_date_delta %>
        </span>

        <% if(toolType === 'translate'){ %>
            <button class="btn btn-info btn-sm up-vote pull-right">
                <% if(voted_by_me){ %>
                <i class="fa fa-thumbs-up"></i>
                <% }else{ %>
                <i class="fa fa-thumbs-o-up"></i>
                <% }%>
                <span><%=vote_count%></span>
            </button>
        <% } %>
        <% if(toolType === 'approve'){ %>
            <% if(!used){ %>
            <button class="btn btn-info btn-sm approve pull-right">
                <i class="fa fa-check"></i>
            </button>
            <% }else{ %>
            <div class="pull-right checked-label">
                <i class="fa fa-check text-success pull-right"></i>
            </div>
            <% } %>
        <% } %>
    </div>
    <%=content %>
</div>