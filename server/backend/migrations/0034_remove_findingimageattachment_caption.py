# Generated by Django 4.2.6 on 2023-11-15 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0033_alter_projectnote_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='findingimageattachment',
            name='caption',
        ),
    ]
