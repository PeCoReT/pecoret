# Generated by Django 5.1.3 on 2024-12-04 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0066_remove_host_project_remove_host_technologies_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customfieldasset',
            name='asset_types',
            field=models.ManyToManyField(blank=True, to='backend.assettype'),
        ),
    ]
