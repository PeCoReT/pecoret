# Generated by Django 4.2.1 on 2023-06-24 08:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0002_initialize_default_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="host",
        ),
        migrations.RemoveField(
            model_name="account",
            name="web_application",
        ),
        migrations.AddField(
            model_name="account",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
