# Generated by Django 5.0.4 on 2024-04-24 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0053_apitoken_scope_knowledgebase'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericasset',
            name='technologies',
            field=models.ManyToManyField(blank=True, to='backend.technology'),
        ),
        migrations.AddField(
            model_name='host',
            name='technologies',
            field=models.ManyToManyField(blank=True, to='backend.technology'),
        ),
        migrations.AddField(
            model_name='mobileapplication',
            name='technologies',
            field=models.ManyToManyField(blank=True, to='backend.technology'),
        ),
        migrations.AddField(
            model_name='thickclient',
            name='technologies',
            field=models.ManyToManyField(blank=True, to='backend.technology'),
        ),
        migrations.AddField(
            model_name='webapplication',
            name='technologies',
            field=models.ManyToManyField(blank=True, to='backend.technology'),
        ),
    ]