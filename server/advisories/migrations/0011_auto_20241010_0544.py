import re

from django.db import migrations


def migrate_attachment_to_image_file(apps, schema_editor):
    ImageFile = apps.get_model('storage', 'ImageFile')
    ImageAttachment = apps.get_model('advisories', 'ImageAttachment')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    for attachment in ImageAttachment.objects.all():
        advisory = attachment.advisory
        ImageFile.objects.create(name=attachment.name,
                                 content_type=ContentType.objects.get_for_model(advisory),
                                 image=attachment.image,
                                 object_id=attachment.advisory.pk)
        regex = f'http.+?/api/advisories/{advisory.pk}/attachments/{attachment.pk}/preview/'
        # find all preview links and replace them with new storage links
        for match in re.finditer(regex, advisory.proof_text):
            matched = match.group(0)
            advisory.proof_text = advisory.proof_text.replace(matched, f'storage:///{attachment.image.name}')
        advisory.save()


class Migration(migrations.Migration):

    dependencies = [
        ('advisories', '0010_sharetoken'),
        ('storage', '0002_imagefile_content_type_imagefile_object_id'),
    ]

    operations = [
        migrations.RunPython(migrate_attachment_to_image_file),
        migrations.DeleteModel(name='ImageAttachment'),
    ]
