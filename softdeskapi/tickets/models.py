from django.db import models
from accounts.models import CustomUser
from app_projects.models import Projects

class Issues(models.Model):

    title = models.CharField()
    description = models.CharField()
    tag = models.CharField()
    priority = models.CharField()
    status = models.CharField()
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE) 
    author_user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE) 
    assignee_user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE) 
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "issues"
        db_table_comment = "Table contenant les différents tickets remontés"
        verbose_name = "Issue"
        verbose_name_plural = "Issues"

class Comments(models.Model):

    description = models.CharField()
    author_user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE) 
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE) 
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comments"
        db_table_comment = "Table contenant les différents commentaires"
        verbose_name = "Issue"
        verbose_name_plural = "Issues"