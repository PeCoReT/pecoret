# Generated by Django 5.1 on 2024-10-05 08:24

import attack_surface.models.finding
import django.core.validators
import django.db.models.deletion
import pecoret.core.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attack_surface', '0003_scantype_alter_service_options_and_more'),
        ('backend', '0063_alter_technology_vendor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Finding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('finding_id', models.CharField(default=attack_surface.models.finding.create_finding_id, max_length=128, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('recommendation', models.TextField(blank=True, null=True)),
                ('severity', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Informational'), (1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Critical')], null=True)),
                ('cvss_score', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(regex='CVSS:3\\.1/AV:[N|A|L|P]/AC:[L|H]/PR:[N|L|H]/UI:[N|R]/S:[C|U]/C:[N|L|H]/I:[N|L|H]/A:[N|L|H]')])),
                ('internal_notes', models.TextField(blank=True, help_text='Internal Notes should not be exposed in custom templates', null=True)),
                ('exploitation_details', models.TextField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Draft'), (1, 'Review Required'), (2, 'Final')], default=0)),
                ('created_by_user', models.ForeignKey(on_delete=pecoret.core.models.CASCADE_USER_TO_GHOST, related_name='created_findings', to=settings.AUTH_USER_MODEL)),
                ('cwe_ids', models.ManyToManyField(blank=True, related_name='as_finding_set', to='backend.cwe')),
                ('edited_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='edited_findings', to=settings.AUTH_USER_MODEL)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_surface.program')),
            ],
            options={
                'ordering': ['-date_created', '-date_updated'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FindingComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Vulnerable'), (1, 'Fixed'), (2, 'Wont Fix')], default=0)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_surface.service')),
                ('finding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_surface.finding')),
            ],
            options={
                'unique_together': {('finding', 'component')},
            },
        ),
    ]