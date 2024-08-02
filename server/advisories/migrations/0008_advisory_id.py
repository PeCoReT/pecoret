import os
import shutil

import django.db.models.deletion
from django.db import migrations, models

import advisories.models.advisory


def map_primary_keys(model):
    for obj in model.objects.all():
        if obj.advisory_id:
            obj.new_advisory = obj.advisory.new_id
            obj.save()


def fill_future_primary_key(apps, schema_editor):
    Advisory = apps.get_model('advisories', 'Advisory')
    for pk, adv in enumerate(Advisory.objects.all()):
        adv.new_id = pk + 1
        labels = []
        for label in adv.labels.all():
            labels.append(str(label.pk))
        adv.temp_labels = ','.join(labels)
        adv.save()

    # map keys
    Comment = apps.get_model('advisories', 'AdvisoryComment')
    Timeline = apps.get_model('advisories', 'AdvisoryTimeline')
    Attachment = apps.get_model('advisories', 'ImageAttachment')
    map_primary_keys(Comment)
    map_primary_keys(Timeline)
    map_primary_keys(Attachment)


def move_attachments(apps, schema_editor):
    Advisory = apps.get_model('advisories', 'Advisory')
    for advisory in Advisory.objects.all():
        if os.path.isdir(f'uploads/advisories/{advisory.advisory_id}/'):
            try:
                shutil.move(f'uploads/advisories/{advisory.advisory_id}/', f'uploads/advisories/{advisory.pk}/')
            except Exception as e:
                print(f'Error moving directory: {e}')


def migrate_label_many_relation(apps, schema_editor):
    Advisory = apps.get_model('advisories', 'Advisory')
    Label = apps.get_model('advisories', 'Label')
    for adv in Advisory.objects.all():
        label_pks = adv.temp_labels.split(',')
        for label_pk in label_pks:
            if not label_pk:
                continue
            label = Label.objects.get(pk=int(label_pk))
            adv.labels.add(label)
            adv.save()


class Migration(migrations.Migration):
    dependencies = [
        ('advisories', '0007_alter_advisory_report_template'),
    ]

    # schema changes will fail on postgres - atomic = False
    atomic = False
    operations = [
        migrations.DeleteModel(
            name='AdvisoryMembership',
        ),
        migrations.AddField(
            model_name='advisory',
            name='new_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='advisory',
            name='temp_labels',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='advisorycomment',
            name='new_advisory',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='advisorytimeline',
            name='new_advisory',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='imageattachment',
            name='new_advisory',
            field=models.BigIntegerField(default=0),
        ),
        migrations.RunPython(fill_future_primary_key),
        migrations.RemoveField(
            model_name='advisorycomment',
            name='advisory',
        ),
        migrations.RemoveField(
            model_name='advisorytimeline',
            name='advisory',
        ),
        migrations.RemoveField(
            model_name='imageattachment',
            name='advisory',
        ),
        migrations.RemoveField(
            model_name='advisory',
            name='labels',
        ),
        migrations.AlterField(
            model_name='advisory',
            name='advisory_id',
            field=models.CharField(default=advisories.models.advisory.create_advisory_id, max_length=28,
                                   primary_key=False, db_column='advisory_id')
        ),
        migrations.AlterField(
            model_name='advisory',
            name='new_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.RenameField(
            model_name='advisorytimeline',
            old_name='new_advisory',
            new_name='advisory',
        ),
        migrations.RenameField(
            model_name='imageattachment',
            old_name='new_advisory',
            new_name='advisory',
        ),
        migrations.RenameField(
            model_name='advisorycomment',
            old_name='new_advisory',
            new_name='advisory',
        ),
        migrations.AlterField(
            model_name='advisorycomment',
            name='advisory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisories.advisory'),
        ),
        migrations.AlterField(
            model_name='advisorytimeline',
            name='advisory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisories.advisory'),
        ),
        migrations.AlterField(
            model_name='imageattachment',
            name='advisory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisories.advisory'),
        ),
        migrations.AddField(
            model_name='advisory',
            name='labels',
            field=models.ManyToManyField(blank=True, to='advisories.label'),
        ),
        migrations.RunPython(migrate_label_many_relation),
        migrations.RenameField(
            model_name='advisory',
            old_name='new_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='advisory',
            name='temp_labels',
        ),
        migrations.AlterField(
            model_name='advisory',
            name='advisory_id',
            field=models.CharField(default=advisories.models.advisory.create_advisory_id, max_length=64),
        ),
        migrations.RunPython(move_attachments)
    ]
