from django.db import migrations, models


def migrate_unique_id(apps, schema_editor):
    Finding = apps.get_model('backend', 'Finding')
    for finding in Finding.objects.filter(unique_id__isnull=True):
        # finding.create_unique_id()
        qs = finding.project.finding_set.order_by('date_created').filter(date_created__lt=finding.date_created)
        count = qs.count() + 1
        finding.unique_id = f'F-{count:05d}'
        finding.save()


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0036_remove_project_require_cvss_base_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='finding',
            name='unique_id',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.RunPython(migrate_unique_id),
        migrations.AlterField(
            model_name='finding',
            name='unique_id',
            field=models.CharField(blank=True, max_length=16, null=False)
        ),
        migrations.AlterUniqueTogether(
            name='finding',
            unique_together={('unique_id', 'project')},
        ),
    ]
