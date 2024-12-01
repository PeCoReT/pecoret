import django
from django.db import migrations, models


def create_asset(apps, component, asset_type, context):
    Asset = apps.get_model("backend", "Asset")
    asset = Asset.objects.create(
        project=component.project,
        accessible=component.accessible,
        environment=component.environment,
        description=component.description,
        asset_type=asset_type,
        **context
    )
    for tech in component.technologies.all():
        asset.technologies.add(tech)
    asset.save()
    return asset


def migrate_components_to_assets(apps, schema_editor):
    WebApplication = apps.get_model("backend", "WebApplication")
    MobileApplication = apps.get_model("backend", "MobileApplication")
    GenericAsset = apps.get_model("backend", "GenericAsset")
    Host = apps.get_model("backend", "Host")
    ThickClient = apps.get_model("backend", "ThickClient")
    ContentType = apps.get_model("contenttypes", "ContentType")
    Finding = apps.get_model("backend", "Finding")
    AssetType = apps.get_model("backend", "AssetType")

    web_asset_type, _ = AssetType.objects.get_or_create(name="Web Application")
    mobile_asset_type, _ = AssetType.objects.get_or_create(name="Mobile Application")
    host_asset_type, _ = AssetType.objects.get_or_create(name="Host")
    generic_asset_type, _ = AssetType.objects.get_or_create(name="Generic Asset")
    thick_asset_type, _ = AssetType.objects.get_or_create(name="Thick Client")
    for webapp in WebApplication.objects.all():
        asset = create_asset(apps, webapp, web_asset_type, {'name': webapp.name})
        ct = ContentType.objects.get_for_model(webapp)
        for finding in Finding.objects.filter(component_content_type=ct, component_object_id=webapp.pk):
            finding.asset = asset
            finding.entrypoint = webapp.base_url
            finding.save()
    for mobile_app in MobileApplication.objects.all():
        asset = create_asset(apps, mobile_app, mobile_asset_type, {'name': mobile_app.name})
        ct = ContentType.objects.get_for_model(mobile_app)
        for finding in Finding.objects.filter(component_content_type=ct, component_object_id=mobile_app.pk):
            finding.asset = asset
            finding.save()
    for host in Host.objects.all():
        asset = create_asset(apps, host, host_asset_type, {'name': str(host)})
        ct = ContentType.objects.get_for_model(host)
        for finding in Finding.objects.filter(component_content_type=ct, component_object_id=host.pk):
            finding.asset = asset
            finding.save()
        for service in host.service_set.all():
            ct = ContentType.objects.get_for_model(service)
            for finding in Finding.objects.filter(component_content_type=ct, component_object_id=service.pk):
                finding.asset = asset
                finding.entrypoint = f'{service.name}://{str(host)}:{service.port}'
                finding.save()

    for generic in GenericAsset.objects.all():
        asset = create_asset(apps, generic, generic_asset_type, {'name': generic.name})
        ct = ContentType.objects.get_for_model(generic)
        for finding in Finding.objects.filter(component_content_type=ct, component_object_id=generic.pk):
            finding.asset = asset
            finding.save()
    for thick in ThickClient.objects.all():
        asset = create_asset(apps, thick, thick_asset_type, {'name': thick.name})
        ct = ContentType.objects.get_for_model(thick)
        for finding in Finding.objects.filter(component_content_type=ct, component_object_id=thick.pk):
            finding.asset = asset
            finding.save()


class Migration(migrations.Migration):
    dependencies = [
        ('backend', '0064_remove_changehistory_user_remove_report_author_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True,
                                                 help_text='Description of the asset type. May be used in your report template.',
                                                 null=True)),
            ],
            options={
                'ordering': ['-date_created', '-date_updated'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='finding',
            name='entrypoint',
            field=models.CharField(help_text='expected to be a URI', max_length=255, null=True, blank=True,
                                   validators=[django.core.validators.URLValidator()]),
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('accessible',
                 models.PositiveSmallIntegerField(choices=[(0, 'Accessible'), (1, 'Not Accessible'), (2, 'Unknown')],
                                                  default=2)),
                ('description', models.TextField(blank=True, null=True)),
                ('environment', models.PositiveSmallIntegerField(
                    choices=[(0, 'Unknown'), (1, 'Production'), (2, 'Testing'), (3, 'Development'), (4, 'Staging')],
                    default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.project')),
                ('technologies', models.ManyToManyField(blank=True, to='backend.technology')),
                ('name', models.CharField(max_length=255)),
                ('asset_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='backend.assettype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='asset',
            unique_together={('name', 'project')},
        ),
        migrations.CreateModel(
            name='CustomFieldAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='the name of the field', max_length=255, unique=True)),
                ('label', models.CharField(help_text='the display label for the field', max_length=255)),
                ('help_text', models.TextField(blank=True, help_text='shown as help text on the field', null=True)),
                ('field_type', models.PositiveIntegerField(
                    choices=[(0, 'char'), (1, 'text'), (2, 'integer'), (3, 'ip'), (4, 'url')])),
                ('max_length',
                 models.PositiveIntegerField(blank=True, help_text='the maximum chars of the field', null=True)),
                ('required', models.BooleanField(default=False, help_text='whether the field is required')),
                ('allow_markdown',
                 models.BooleanField(default=False, help_text='whether the field is allowed to be markdown')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomFieldAssetValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('value', models.TextField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.asset')),
                (
                    'field',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.customfieldasset')),
            ],
            options={
                'unique_together': {('asset', 'field')},
            },
        ),

        migrations.AddField(
            model_name='finding',
            name='asset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.asset'),
        ),
        migrations.RunPython(migrate_components_to_assets),
        migrations.RemoveIndex(
            model_name='finding',
            name='backend_fin_compone_af25d2_idx',
        ),
        migrations.RemoveField(
            model_name='finding',
            name='component_content_type',
        ),
        migrations.RemoveField(
            model_name='finding',
            name='component_object_id',
        ),
    ]
