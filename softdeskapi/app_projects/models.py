from django.db import models
from accounts.models import CustomUser

class Projects(models.Model):

    TYPE_CHOICES = [
        ("BE", "Back-End"),
        ("FE", "Front-End"),
        ("IOS", "IOS"),
        ("AD", "Android"),
    ]
    
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "projects"
        db_table_comment = "Table contenant les différents projets"
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title


class Contributors(models.Model):

    PERMISSIONS_CHOICES = [
        ("AUT", "Author"),
        ("CON", "Contributor"),
    ]

    project_id = models.ForeignKey(
        to=Projects, on_delete=models.CASCADE, null=True, blank=True) # See
    author_user_id = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, null=True, blank=True) # See

    permission = models.CharField(max_length=3, choices=PERMISSIONS_CHOICES)
    role = models.CharField(max_length=255)

    class Meta:
        db_table = "contributors"
        db_table_comment = "Table contenant les différents participants"
        verbose_name = "Contributor"
        verbose_name_plural = "Contributors"



        