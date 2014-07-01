<div class="user-profile-card popover-hover">
    <a href="/personal/<%=user_id %>" class="avatar">
        <img src="<%=avatar_url %>" alt="<%=nickname %>"/>
    </a>
    <div class="card-content">
        <div class="card-heading">
            <div class="nickname">
                <a href="/personal/<%=user_id %>" title="<%=nickname %>">
                    <strong>
                        <%=nickname %>
                    </strong>
                </a>
            </div>
            <div class="user-level">
                <a href="javascript:void(0);" title="初出茅庐">
                    <i class="fa fa-star"></i>
                    <i class="fa fa-star"></i>
                    <i class="fa fa-star"></i>
                </a>
            </div>
        </div>
        <div class="card-body">

        </div>
    </div>
    <div class="contact-btns meta">
        <a class="mail " href="/mail/write?to=<%=user_id %>" target="_blank">
            <i class="fa fa-envelope-o"></i> 发站内信
        </a>
        <% if(followed){ %>
            <a class="follow" href="javascript: void(0);" data-user_id="<%=user_id %>" data-loading-text="正在提交...">
                <i class="fa fa-minus"></i> 取消关注
            </a>
        <% } else { %>
            <a class="follow" href="javascript: void(0);" data-user_id="<%=user_id %>" data-loading-text="正在提交...">
                <i class="fa fa-plus"></i> 关注
            </a>
        <% } %>
    </div>
</div>