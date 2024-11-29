from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0065_assettype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assettype',
            name='description',
            field=models.TextField(blank=True, help_text='Description of the asset type. May be used in your report template.', null=True),
        ),
    ]
