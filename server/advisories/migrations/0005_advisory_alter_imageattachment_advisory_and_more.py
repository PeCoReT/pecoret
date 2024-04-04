import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import advisories.models.advisory
import pecoret.core.models


class Migration(migrations.Migration):
    dependencies = [
        ('advisories', '0004_advisory_alter_imageattachment_advisory'),
        ('backend', '0051_alter_advisorymembership_advisory_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Advisory',
                    fields=[
                        ('date_created', models.DateTimeField(auto_now_add=True)),
                        ('date_updated', models.DateTimeField(auto_now=True)),
                        ('advisory_id',
                         models.CharField(default=advisories.models.advisory.create_advisory_id, max_length=28,
                                          primary_key=True, serialize=False)),
                        ('date_planned_disclosure', models.DateField()),
                        ('date_disclosure', models.DateField(blank=True, null=True)),
                        ('internal_name', models.CharField(default='', max_length=64)),
                        ('affected_versions', models.CharField(max_length=128)),
                        ('fixed_version', models.CharField(blank=True, max_length=128, null=True)),
                        ('severity', models.PositiveSmallIntegerField(
                            choices=[(0, 'Informational'), (1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Critical')])),
                        ('cve_id', models.CharField(blank=True, max_length=20, null=True)),
                        ('description', models.TextField(blank=True, null=True)),
                        ('recommendation', models.TextField(blank=True, null=True)),
                        ('custom_report_title', models.CharField(blank=True, max_length=255, null=True)),
                        ('hide_advisory_id_in_report', models.BooleanField(default=False)),
                        ('proof_text', models.TextField(blank=True, default='')),
                        ('status',
                         models.PositiveSmallIntegerField(choices=[(1, 'Not Disclosed'), (2, 'Disclosed')], default=1)),
                        ('vulnerability_status',
                         models.PositiveSmallIntegerField(choices=[(1, 'Unfixed'), (2, 'Fixed'), (3, "Won't Fix")],
                                                          default=1)),
                        ('visibility',
                         models.PositiveSmallIntegerField(choices=[(1, 'Members'), (2, 'Team')], default=1)),
                        ('researchers', models.CharField(blank=True, max_length=512, null=True)),
                        ('labels', models.ManyToManyField(blank=True, to='advisories.label')),
                        ('report_template',
                         models.ForeignKey(default=advisories.models.advisory.default_report_template,
                                           on_delete=pecoret.core.models.CASCADE_REPORT_TEMPLATE_DEFAULT,
                                           to='backend.reporttemplate')),
                        ('technology',
                         models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='backend.technology')),
                        ('user',
                         models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                        ('vulnerability', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                                            to='backend.vulnerabilitytemplate')),
                    ],
                    options={
                        'db_table': 'backend_advisory',
                        'ordering': ['-advisory_id', 'date_updated'],
                    },
                ),
                migrations.AlterField(
                    model_name='imageattachment',
                    name='advisory',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisories.advisory'),
                ),
                migrations.CreateModel(
                    name='AdvisoryComment',
                    fields=[
                        ('id',
                         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('date_created', models.DateTimeField(auto_now_add=True)),
                        ('date_updated', models.DateTimeField(auto_now=True)),
                        ('comment', models.TextField()),
                        ('advisory',
                         models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisories.advisory')),
                        ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                   to=settings.AUTH_USER_MODEL)),
                        ('user_edit',
                         models.ForeignKey(blank=True, null=True, on_delete=pecoret.core.models.CASCADE_USER_TO_GHOST,
                                           related_name='advisory_comment_edited_set', to=settings.AUTH_USER_MODEL)),
                    ],
                    options={
                        'db_table': 'backend_advisorycomment',
                        'ordering': ['date_created'],
                    },
                ),
                migrations.CreateModel(
                    name='AdvisoryTimeline',
                    fields=[
                        ('id',
                         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('date', models.DateField()),
                        ('text', models.CharField(max_length=255)),
                        ('advisory',
                         models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisories.advisory')),
                    ],
                    options={
                        'db_table': 'backend_advisorytimeline',
                        'ordering': ['-date'],
                    },
                ),
                migrations.CreateModel(
                    name='AdvisoryMembership',
                    fields=[
                        ('id',
                         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('date_created', models.DateTimeField(auto_now_add=True)),
                        ('date_updated', models.DateTimeField(auto_now=True)),
                        ('active_until', models.DateTimeField(blank=True, default=None, null=True)),
                        ('role',
                         models.PositiveSmallIntegerField(choices=[(0, 'Creator'), (1, 'Read Only'), (2, 'Vendor')],
                                                          default=1)),
                        ('advisory',
                         models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisories.advisory')),
                        ('user',
                         models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                    ],
                    options={
                        'db_table': 'backend_advisorymembership',
                        'ordering': ['-date_created'],
                        'unique_together': {('user', 'advisory')},
                    },
                ),
            ],
            database_operations=[]
        )

    ]
