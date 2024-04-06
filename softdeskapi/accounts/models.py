from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from accounts.path_and_rename import PathAndRename


class CustomUser(AbstractUser):

    birthday = models.DateField()
    can_be_contacted = models.BooleanField(default=False)
    sharing_data = models.BooleanField(default=False)

    profile_pic = models.ImageField(null=False, blank=True, upload_to=PathAndRename('profile_pic'))

    IMAGE_MAX_SIZE = (200, 200)

    def resize_image(self):
        image = Image.open(self.profile_pic)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.profile_pic.path)

    def save(self, *args, **kwargs):
        try:
            myUser = CustomUser.objects.get(id=self.pk)
            if myUser.profile_pic != self.profile_pic:
                myUser.profile_pic.delete(save=False)
        except Exception:
            pass

        super().save(*args, **kwargs)
        if self.profile_pic:
            self.resize_image()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
