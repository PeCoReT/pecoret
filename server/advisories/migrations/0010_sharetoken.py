# Generated by Django 5.0.7 on 2024-08-05 04:20

import advisories.models.share_token
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisories', '0009_remove_advisory_visibility'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('token', models.CharField(default=advisories.models.share_token.generate_token, max_length=255, unique=True)),
                ('date_expire', models.DateTimeField(blank=True, null=True)),
                ('advisory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisories.advisory')),
            ],
            options={
                'ordering': ['-date_created'],
                'unique_together': {('name', 'advisory')},
            },
        ),
    ]