# Generated by Django 5.0 on 2024-01-04 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0039_finding_cvss_score_31_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finding',
            name='authenticated_test',
        ),
    ]
