# Generated by Django 5.1.7 on 2025-03-14 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_upload', '0002_remove_image_image_image_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='jsonData',
            field=models.JSONField(default=dict),
        ),
    ]
