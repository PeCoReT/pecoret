# Generated by Django 4.2.1 on 2023-07-15 10:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0009_advisory_custom_report_title_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="require_owasp_risk_rating",
            field=models.BooleanField(default=False),
        ),
    ]
