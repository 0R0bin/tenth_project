# Generated by Django 4.2.2 on 2023-07-17 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contributors',
            old_name='author_user_id',
            new_name='author_user',
        ),
        migrations.RenameField(
            model_name='contributors',
            old_name='project_id',
            new_name='project',
        ),
    ]
