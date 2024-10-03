import django.core.validators
import django.db.models.deletion
import secrets
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attack_surface', '0002_rewrite'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScanType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. Port scan, tech detection, ...', max_length=255, unique=True, validators=[django.core.validators.RegexValidator(regex='^[A-Za-z0-9\\-]+$')])),
                ('description', models.TextField(blank=True, null=True)),
                ('can_run_manually', models.BooleanField(default=True)),
                ('allowed_object_type', models.CharField(choices=[('host', 'Host'), ('port', 'Port'), ('service', 'Service'), ('target', 'Target'), ('url', 'URL')], max_length=64)),
                ('conditions', models.TextField(blank=True, null=True)),
                ('priority', models.PositiveSmallIntegerField(default=5)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-priority', 'name'],
            },
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-date_updated']},
        ),
        migrations.AddField(
            model_name='service',
            name='uses_encryption',
            field=models.BooleanField(default=False, help_text='Uses TLS/SSL encryption'),
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
        migrations.AlterField(
            model_name='service',
            name='port_number',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(65535)]),
        ),
        migrations.AlterField(
            model_name='service',
            name='port_status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Open'), (1, 'Closed')], default=0),
        ),
        migrations.AlterField(
            model_name='service',
            name='protocol',
            field=models.PositiveSmallIntegerField(choices=[(0, 'TCP'), (1, 'UDP')], default=0),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_name',
            field=models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9]+$')]),
        ),
        migrations.AlterField(
            model_name='target',
            name='asn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='attack_surface.asn'),
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('scan_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'Running'), (2, 'Completed'), (3, 'Failed')], default=0)),
                ('output', models.TextField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('job_id', models.CharField(blank=True, help_text='Job ID received from rq', max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('scan_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attack_surface.scantype')),
            ],
            options={
                'ordering': ['-date_created', '-date_updated'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScanObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('scan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_surface.scan')),
            ],
        ),
        migrations.CreateModel(
            name='Scanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('token', models.CharField(default=secrets.token_urlsafe, editable=False, max_length=255)),
                ('scan_types', models.ManyToManyField(to='attack_surface.scantype')),
            ],
            options={
                'ordering': ['-date_created', '-date_updated'],
                'abstract': False,
            },
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
