<form action="/task/task_preview" target="_blank" method="post">
    <input type="hidden" name="task_name" value="<%=task_name %>" id="task_name"/>
    <textarea name="task_content" id="task_content"><%=task_content %></textarea>
    <input type="hidden" name="status" value="<%=status %>" id="status"/>
    <input type="hidden" name="tags" value="<%=tags %>" id="tags"/>
</form>