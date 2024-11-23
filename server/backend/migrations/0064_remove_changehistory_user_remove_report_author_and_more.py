from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0063_alter_technology_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='changehistory',
            name='user',
        ),
        migrations.RemoveField(
            model_name='report',
            name='author',
        ),
        migrations.RemoveField(
            model_name='usersettings',
            name='show_real_name_in_report',
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
