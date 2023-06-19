from django.contrib import admin
from app_projects.models import Projects, Contributors


class ProjectsAdmin(admin.ModelAdmin):

    list_display = ('title', 'description', 'type', 'created_time')
    
class ContributorsAdmin(admin.ModelAdmin):

    list_display = ('project_id', 'author_user_id', 'permission', 'role')


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Contributors, ContributorsAdmin)
