# Generated by Django 4.2.8 on 2023-12-25 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='important',
            field=models.BooleanField(default=False),
        ),
    ]
