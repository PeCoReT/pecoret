# Generated by Django 5.0.7 on 2024-08-02 05:55

from django.db import migrations


def delete_adv_management_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    g = Group.objects.filter(name='Advisory Management')
    if g.exists():
        g.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0061_delete_authtoken'),
    ]

    operations = [
        migrations.RunPython(delete_adv_management_group)
    ]