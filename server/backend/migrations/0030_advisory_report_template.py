import advisories.models.advisory
from django.db import migrations, models
import pecoret.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0029_user_new_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisory',
            name='report_template',
            field=models.ForeignKey(default=1, on_delete=models.CASCADE, to='backend.reporttemplate'),
        ),
    ]
