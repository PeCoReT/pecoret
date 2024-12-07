# Generated by Django 5.1.3 on 2024-11-30 15:39

import django.db.models.deletion
from django.db import migrations, models


def migrate_components_to_assets(apps, schema_editor):
    Host = apps.get_model("backend", "Host")
    Asset = apps.get_model("backend", "Asset")
    AssetChecklist = apps.get_model("checklists", "AssetChecklist")
    for checklist in AssetChecklist.objects.all():
        # asset should already exist because of previous migration
        if isinstance(checklist.component, Host):
            name = str(checklist.component)
        else:
            name = checklist.component.name
        asset = Asset.objects.get(project=checklist.project, asset_type=checklist.component.asset_type, name=name)
        checklist.asset = asset
        checklist.save()


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0065_assettype'),
        ('checklists', '0007_alter_assetcategory_category_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetchecklist',
            name='asset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.asset'),
        ),
        migrations.RunPython(migrate_components_to_assets),
        migrations.AlterField(
            model_name='assetchecklist',
            name='asset',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, to='backend.asset'),
        ),
        migrations.RemoveIndex(
            model_name='assetchecklist',
            name='checklists__compone_460dff_idx',
        ),
        migrations.RemoveField(
            model_name='assetchecklist',
            name='component_content_type',
        ),
        migrations.RemoveField(
            model_name='assetchecklist',
            name='component_object_id',
        ),
    ]
