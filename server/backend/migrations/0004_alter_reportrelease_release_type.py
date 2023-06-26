# Generated by Django 4.2.1 on 2023-06-25 18:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0003_remove_account_host_remove_account_web_application_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reportrelease",
            name="release_type",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Draft"), (1, "Final"), (2, "Preview")]
            ),
        ),
    ]
