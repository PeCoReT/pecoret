import django.core.validators
import django.db.models.deletion
import secrets
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attack_surface', '0002_rewrite'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
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
            ],
            options={
                'ordering': ['-date_created', '-date_updated'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScanType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. Port scan, tech detection, ...', max_length=255, unique=True, validators=[django.core.validators.RegexValidator(regex='^[A-Za-z0-9\\-]+$')])),
                ('description', models.TextField(blank=True, null=True)),
                ('can_run_manually', models.BooleanField(default=True)),
                ('allowed_object_type', models.CharField(choices=[('host', 'Host'), ('port', 'Port'), ('service', 'Service'), ('target', 'Target'), ('url', 'URL')], max_length=64)),
                ('conditions', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-date_updated']},
        ),
        migrations.AddField(
            model_name='port',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Open'), (1, 'Closed')], default=0),
        ),
        migrations.AlterField(
            model_name='host',
            name='ip_address',
            field=models.GenericIPAddressField(unique=True),
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
        migrations.AddField(
            model_name='scan',
            name='scan_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attack_surface.scantype'),
        ),
    ]
