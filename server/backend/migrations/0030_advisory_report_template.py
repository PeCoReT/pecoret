import backend.models.advisory
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
            field=models.ForeignKey(default=backend.models.advisory.default_report_template, on_delete=pecoret.core.models.CASCADE_REPORT_TEMPLATE_DEFAULT, to='backend.reporttemplate'),
        ),
    ]
