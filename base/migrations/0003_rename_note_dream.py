# Generated by Django 4.2.8 on 2024-01-26 10:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_note_important'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Note',
            new_name='Dream',
        ),
    ]
