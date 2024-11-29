
from django.db import migrations, models


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
                ('description', models.CharField(blank=True, help_text='Description of the asset type. May be used in your report template.', max_length=255, null=True)),
            ],
            options={
                'ordering': ['-date_created', '-date_updated'],
                'abstract': False,
            },
        ),
    ]
