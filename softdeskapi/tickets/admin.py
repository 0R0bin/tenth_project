from django.contrib import admin
from tickets.models import Issues, Comments



class IssuesAdmin(admin.ModelAdmin):

    list_display = ('title', 'description', 'tag', 'priority', 'status', 'project_id', 'author_user_id', 'assignee_user_id')

class CommentsAdmin(admin.ModelAdmin):

    list_display = ('description', 'author_user_id', 'issue_id', 'created_time')


admin.site.register(Issues, IssuesAdmin)
admin.site.register(Comments, CommentsAdmin)