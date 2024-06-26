import uuid
from django.db import models
from accounts.models import CustomUser
from app_projects.models import Projects


class Issues(models.Model):

    TAG_CHOICES = [
        ("B", "Bug"),
        ("UP", "Amélioration"),
        ("TODO", "Tâche"),
    ]
    PRIORITY_CHOICES = [
        ("0", "Faible"),
        ("1", "Moyenne"),
        ("2", "Élevée"),
    ]
    STATUS_CHOICES = [
        ("0", "À Faire"),
        ("1", 'En Cours'),
        ("2", "Terminé"),
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tag = models.CharField(max_length=4, choices=TAG_CHOICES)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="0")
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    author_user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='author')
    assignee_user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                                      related_name='assignee', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "issues"
        db_table_comment = "Table contenant les différents tickets remontés"
        verbose_name = "Issue"
        verbose_name_plural = "Issues"

    def __str__(self):
        return self.title


class Comments(models.Model):

    description = models.CharField(max_length=255)
    author_user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, primary_key=False, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comments"
        db_table_comment = "Table contenant les différents commentaires"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
