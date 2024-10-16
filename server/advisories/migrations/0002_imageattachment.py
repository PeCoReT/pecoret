# Generated by Django 4.2.4 on 2023-08-21 03:58

from django.db import migrations, models
import django.db.models.deletion


def migrate_proofs(apps, schema_editor):
    from django.core.files.images import ImageFile
    from django.conf import settings
    from django.urls import reverse
    Advisory = apps.get_model("backend.Advisory")
    Attachment = apps.get_model("advisories.ImageAttachment")
    for finding in Advisory.objects.all():
        proofs = finding.advisoryproof_set.all()
        proof_text = ""
        for proof in proofs:
            proof_text += f"{proof.text}\n"
            if proof.image_caption:
                image_file = ImageFile(proof.image)
                attachment = Attachment.objects.create(advisory=finding, image=image_file,
                                                       caption=proof.image_caption)
                attachment.name = proof.title
                attachment.save()
                attachment_url = reverse("backend:advisories:attachment-preview", kwargs={
                    'advisory': finding.pk,
                    'pk': attachment.pk
                })
                proof_text += f"![{proof.title}]({settings.PROTOCOL}://{settings.DOMAIN}{attachment_url})\n"
        finding.proof_text = proof_text
        finding.save()


class Migration(migrations.Migration):
    dependencies = [
        ('backend', '0018_alter_finding_proof_text'),
        ('advisories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(max_length=256)),
                ('name', models.CharField(max_length=128)),
                ('caption', models.CharField(blank=True, max_length=256, null=True)),
                ('advisory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.advisory')),
            ],
            options={
                'ordering': ['-date_updated'],
            },
        ),
        migrations.RunPython(migrate_proofs)
    ]
