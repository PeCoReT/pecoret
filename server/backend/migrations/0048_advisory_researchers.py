# Generated by Django 5.0.3 on 2024-03-27 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0047_technology_apitoken_scope_asmonitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisory',
            name='researchers',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
