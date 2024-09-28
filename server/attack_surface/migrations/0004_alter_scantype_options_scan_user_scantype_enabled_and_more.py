import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attack_surface', '0003_scan_scantype_alter_service_options_port_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scantype',
            options={'ordering': ['-priority', 'name']},
        ),
        migrations.AddField(
            model_name='scan',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scantype',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='scantype',
            name='priority',
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='url',
            name='favicon_hash',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='url',
            name='fuzzy_hash_body',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='url',
            name='fuzzy_hash_headers',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.CreateModel(
            name='UserSearchQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('query', models.CharField(max_length=1024)),
                ('name', models.CharField(max_length=28)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('user', 'name')},
            },
        ),
    ]
