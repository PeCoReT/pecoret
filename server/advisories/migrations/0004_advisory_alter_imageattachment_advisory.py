import advisories.models.advisory
import django.db.models.deletion
import pecoret.core.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisories', '0003_remove_imageattachment_caption'),
        ('backend', '0050_alter_advisory_technology'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
    ]
