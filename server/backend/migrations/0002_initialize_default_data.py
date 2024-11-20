from django.db import migrations


def initialize_default_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    groups = ["Management", "Pentester", "Customer"]
    for group in groups:
        Group.objects.get_or_create(name=group)


def initialize_default_user(apps, schema_editor):
    User = apps.get_model('backend', 'User')
    User.objects.get_or_create(username="Ghost", is_active=False)


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(initialize_default_groups),
        migrations.RunPython(initialize_default_user),
    ]
