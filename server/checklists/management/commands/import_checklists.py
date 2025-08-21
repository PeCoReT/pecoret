from pathlib import Path
import yaml
from django.core.management.base import BaseCommand
from checklists import models


class Command(BaseCommand):
    help = "Import checklists from directory into PeCoReT"

    def add_arguments(self, parser):
        parser.add_argument("directory")

    def import_categories(self, directory):
        task_path = Path(directory) / "categories"
        for path in Path(task_path).rglob("*.yaml"):
            items_directory = Path(directory) / "items"
            # read category file
            with open(path, "r", encoding="utf-8") as my_file:
                category_yaml = yaml.safe_load(my_file)
            category, _created = models.Category.objects.update_or_create(
                category_id=category_yaml["id"],
                defaults={
                    "name": category_yaml["name"],
                    "summary": category_yaml.get("summary"),
                },
            )
            self.import_category_items(
                category_yaml.get("items", []), category, items_directory
            )

    def import_category_items(self, item_ids, category, directory):
        for item_id in item_ids:
            items_directory = Path(directory)
            item_files = list(items_directory.rglob(f"{item_id}.md"))
            if not item_files:
                continue
            item_file = item_files[0]
            with open(item_file, "r", encoding="utf-8") as my_file:
                models.Item.objects.update_or_create(
                    category=category,
                    item_id=item_id,
                    defaults={"name": item_id, "description": my_file.read()},
                )

    def import_checklists(self, directory):
        checklist_path = Path(directory) / "lists"
        for path in Path(checklist_path).rglob("*.yaml"):
            with open(path, "r", encoding="utf-8") as my_file:
                yaml_data = yaml.safe_load(my_file)
            for data in yaml_data:
                checklist, _created = models.Checklist.objects.update_or_create(
                    checklist_id=data["id"], defaults={"name": data["name"]}
                )
                category_names = data["categories"]
                categories = models.Category.objects.filter(
                    category_id__in=category_names
                )
                for category in categories:
                    checklist.categories.add(category)
                    checklist.save()

    def handle(self, *args, **options):
        directory = options["directory"]
        self.import_categories(directory)
        self.import_checklists(directory)
