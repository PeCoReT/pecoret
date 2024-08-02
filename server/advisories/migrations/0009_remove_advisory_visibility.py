from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advisories', '0008_advisory_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advisory',
            name='visibility',
        ),
    ]
