import os
from defusedxml import ElementTree as DET
from django.conf import settings
from django.core.management.base import BaseCommand
from backend.models import CWE
from backend.models.cwe import EntryType


class Command(BaseCommand):
    help = "Import cwe entries"
    cwe_version = "4.12"
    namespace = "http://cwe.mitre.org/cwe-7"

    def handle(self, *args, **options):
        tree = DET.parse(
            os.path.join(settings.BASE_DIR, "resources/cwec_v%s.xml" % self.cwe_version)
        )
        root = tree.getroot()
        for weakness in root.iter("{%s}Weakness" % self.namespace):
            cwe_id = weakness.attrib["ID"]
            description = None
            extended_description = None
            name = weakness.attrib.get("Name")
            for child in weakness:
                if child.tag == "{%s}Description" % self.namespace:
                    description = child.text
                elif child.tag == "{%s}Extended_Description" % self.namespace:
                    extended_description = child.text
            if not extended_description:
                extended_description = ""
            CWE.objects.update_or_create(
                cwe_id=cwe_id,
                defaults={
                    "name": name,
                    "description": description,
                    "extended_description": extended_description,
                    "entry_type": EntryType.WEAKNESS,
                },
            )
