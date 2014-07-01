<div class="row-wrapper">
    <% if(!(toolType == 'read' && read_mode == 'result')){ %>
    <div class="col-md-<%=toolType == 'read' && read_mode == 'origin'? '12':'6' %> entry">
        <%=entry.highlighted_word || entry.word %>
    </div>
    <% } %>
    <% if(!(toolType == 'read' && read_mode == 'origin')){ %>
    <div class="col-md-<%=toolType == 'read' && read_mode == 'result'? '12':'6' %> result">
        <% if(result){ %>
        <% if(result.used){ %>
        <div class="used-or-not-label" title="已确认">
            <i class="fa fa-check text-success"></i>
        </div>
        <% } %>
        <%=result.content %>
        <% }else if(toolType == 'read' && read_mode == 'result'){ %>
                        <span class="no-result">
                            <%=entry.word %>
                        </span>
        <% } %>
    </div>
    <% } %>
</div>