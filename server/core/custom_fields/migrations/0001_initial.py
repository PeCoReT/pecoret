from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='the name of the field', max_length=255, unique=True)),
                ('label', models.CharField(help_text='the display label for the field', max_length=255)),
                ('help_text', models.TextField(blank=True, help_text='shown as help text on the field', null=True)),
                ('field_type', models.PositiveIntegerField(choices=[(0, 'Char'), (1, 'Text'), (2, 'Integer')])),
                ('max_length', models.PositiveIntegerField(blank=True, help_text='the maximum chars of the field', null=True)),
                ('required', models.BooleanField(default=False, help_text='whether the field is required')),
                ('allow_markdown', models.BooleanField(default=False, help_text='whether the field is allowed to be markdown')),
            ],
            options={
                'ordering': ['-date_created', '-date_updated'],
                'abstract': False,
            },
        ),
    ]
