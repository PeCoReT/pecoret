# Generated by Django 5.0.4 on 2024-05-30 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0058_alter_technology_cpe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apitoken',
            old_name='scope_asmonitor',
            new_name='scope_attack_surface',
        ),
    ]
