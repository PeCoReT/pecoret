# Generated by Django 5.1 on 2024-10-09 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attack_surface', '0004_finding_findingcomponent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='findingcomponent',
            options={'ordering': ['-date_updated']},
        ),
    ]
