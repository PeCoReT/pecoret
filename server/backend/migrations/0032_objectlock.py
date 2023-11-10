from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('backend', '0031_projectnote'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectLock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_seen', models.DateTimeField(auto_now_add=True)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveSmallIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to=models.Q(('app_label', 'backend'), ('model', 'projectnote')), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-last_seen'],
                'indexes': [models.Index(fields=['content_type', 'object_id'], name='backend_obj_content_48fb8c_idx')],
                'unique_together': {('content_type', 'object_id')},
            },
        ),
    ]
