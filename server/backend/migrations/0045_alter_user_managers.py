# Generated by Django 5.0.1 on 2024-01-28 08:49

import backend.models.user
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0044_user_company'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', backend.models.user.UserManager()),
            ],
        ),
    ]
