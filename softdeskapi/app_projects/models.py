from django.db import models
from accounts.models import CustomUser

class Projects(models.Model):

    title = models.CharField()
    description = models.CharField()
    type = models.CharField()
    created_time = models.DateTimeField(auto_now_add=True)
    author_user_id = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, null=True, blank=True) # See

    class Meta:
        db_table = "projects"
        db_table_comment = "Table contenant les différents projets"
        verbose_name = "Project"
        verbose_name_plural = "Projects"

class Contributors(models.Model):

    title = models.CharField()
    description = models.CharField()
    type = models.CharField()
    created_time = models.DateTimeField(auto_now_add=True)
    author_user_id = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, null=True, blank=True) # See

    class Meta:
        db_table = "projects"
        db_table_comment = "Table contenant les différents projets"
        verbose_name = "Project"
        verbose_name_plural = "Projects"

        