from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asmonitor', '0006_url_is_base'),
    ]

    operations = [
        migrations.AddField(
            model_name='finding',
            name='internal_information',
            field=models.TextField(blank=True, null=True),
        ),
    ]
