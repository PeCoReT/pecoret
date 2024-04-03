from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('advisories', '0005_advisory_alter_imageattachment_advisory_and_more'),
        ('backend', '0051_alter_advisorymembership_advisory_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='advisorymembership',
                    name='advisory',
                ),
                migrations.RemoveField(
                    model_name='advisorycomment',
                    name='advisory',
                ),
                migrations.RemoveField(
                    model_name='advisorytimeline',
                    name='advisory',
                ),
                migrations.RemoveField(
                    model_name='advisorycomment',
                    name='user',
                ),
                migrations.RemoveField(
                    model_name='advisorycomment',
                    name='user_edit',
                ),
                migrations.AlterUniqueTogether(
                    name='advisorymembership',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='advisorymembership',
                    name='user',
                ),
                migrations.DeleteModel(
                    name='Advisory',
                ),
                migrations.DeleteModel(
                    name='AdvisoryTimeline',
                ),
                migrations.DeleteModel(
                    name='AdvisoryComment',
                ),
                migrations.DeleteModel(
                    name='AdvisoryMembership',
                ),
            ],
            database_operations=[]
        )

    ]
