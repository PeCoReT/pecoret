import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attack_surface', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(name='Program'),
        migrations.DeleteModel(name='Tag'),
        migrations.DeleteModel(name='Port'),
        migrations.DeleteModel(name='ScanFinding'),
        migrations.DeleteModel(name='Target'),
        migrations.DeleteModel(name='URL'),
        migrations.CreateModel(
            name='ASN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(max_length=255)),
                ('country_code', models.CharField(max_length=8)),
                ('region', models.CharField(max_length=255)),
                ('region_name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('zipcode', models.CharField(blank=True, max_length=32, null=True)),
                ('timezone', models.CharField(blank=True, max_length=128, null=True)),
                ('isp', models.CharField(blank=True, max_length=255, null=True)),
                ('organization', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=32, unique=True, validators=[django.core.validators.RegexValidator(regex='^AS[0-9]+$')])),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('color', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(regex='#([a-fA-F\\d]{6}|[a-fA-F\\d]{3})')])),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('date_asn_last_updated', models.DateTimeField(blank=True, null=True)),
                ('asn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='attack_surface.asn')),
            ],
            options={
                'ordering': ['-date_created', '-date_updated'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('number', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(65535)])),
                ('service_name', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9]+$')])),
                ('protocol', models.PositiveSmallIntegerField(choices=[(0, 'TCP'), (1, 'UDP')], default=0)),
                ('uses_encryption', models.BooleanField(default=False, help_text='Uses TLS/SSL encryption')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_surface.host')),
            ],
            options={
                'ordering': ['number', 'protocol'],
                'unique_together': {('host', 'number', 'protocol')},
            },
        ),
        migrations.CreateModel(
            name='ScanFinding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('tool', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=512)),
                ('affected_component', models.CharField(max_length=1024)),
                ('result', models.TextField()),
                ('full_output', models.TextField(blank=True, null=True)),
                ('false_positive', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('severity', models.PositiveSmallIntegerField(choices=[(0, 'Informational'), (1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Critical')])),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Open'), (2, 'Closed')], default=0)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_surface.program')),
            ],
            options={
                'ordering': ['-date_created', '-severity'],
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('data', models.CharField(db_index=True, max_length=512)),
                ('scope', models.PositiveSmallIntegerField(choices=[(0, 'In Scope'), (1, 'Undefined'), (2, 'Out of Scope')], default=1)),
                ('description', models.TextField(blank=True, null=True)),
                ('data_type', models.PositiveSmallIntegerField(choices=[(0, 'IP'), (2, 'Domain'), (3, 'Subdomain')])),
                ('host', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='attack_surface.host')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_surface.program')),
            ],
            options={
                'ordering': ['-date_updated', 'data'],
                'unique_together': {('data', 'program')},
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('banner', models.TextField(blank=True, null=True)),
                ('cert_issuer', models.CharField(blank=True, max_length=255, null=True)),
                ('cert_subject', models.CharField(blank=True, max_length=255, null=True)),
                ('cert_valid_from', models.DateTimeField(blank=True, null=True)),
                ('cert_expiry', models.DateTimeField(blank=True, null=True)),
                ('cert_fingerprint', models.CharField(blank=True, max_length=64, null=True)),
                ('cert_public_key_info', models.CharField(blank=True, max_length=255, null=True)),
                ('cert_san', models.TextField(blank=True, null=True)),
                ('port', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_surface.port')),
                ('technologies', models.ManyToManyField(blank=True, to='backend.technology')),
                ('tags', models.ManyToManyField(blank=True, to='attack_surface.tag')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_surface.target')),
            ],
            options={
                'unique_together': {('port', 'target')},
            },
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('url', models.URLField()),
                ('request', models.TextField(blank=True, null=True)),
                ('response', models.TextField(blank=True, null=True)),
                ('status_code', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('is_base', models.BooleanField(editable=False)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_surface.service')),
                ('tags', models.ManyToManyField(blank=True, to='attack_surface.tag')),
                ('technologies', models.ManyToManyField(blank=True, to='backend.technology')),
            ],
            options={
                'ordering': ['-date_updated', 'url'],
                'unique_together': {('service', 'url')},
            },
        ),
    ]
