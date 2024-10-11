# Generated by Django 5.1 on 2024-10-10 05:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagefile',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='imagefile',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
