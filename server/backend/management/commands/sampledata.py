from pathlib import Path

import yaml
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand

from asmonitor import models as asmonitor_models
from backend import models
from backend.models.membership import Roles
from backend.models.project import TestMethod
from backend.models.finding import Severity
from checklists.models import Category, Item, Checklist


class Command(BaseCommand):
    help = 'populate database with some sample data'
    data = None

    def handle(self, *args, **options):
        self.stdout.write('Importing CWE entries...')
        call_command('import_cwe_entries')
        self.stdout.write('Init cronjobs...')
        call_command('init_default_cronjobs')
        directory = Path(settings.BASE_DIR / 'resources/sample_data')
        for path in sorted(Path(directory).rglob('*.yaml')):
            self.stdout.write(f'Reading data from {path}')
            with open(path, 'r') as f:
                self.data = yaml.safe_load(f)
            self.create_users()
            self.create_project_types()
            self.create_companies()
            self.create_projects()
            self.create_checklists()
            self.create_technologies()
            self.create_attack_surface_data()

    def create_users(self):
        self.stdout.write('Creating users...')
        for item in self.data.get('users', []):
            name = item.pop('username')
            password = item.pop('password')
            groups = item.pop('groups', [])
            user, created = models.User.objects.get_or_create(username=name, defaults=item)
            if created:
                user.set_password(password)
            for group_name in groups:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            user.save()

    def create_project_types(self):
        self.stdout.write('Creating project types...')
        for item in self.data.get('project-types', []):
            name = item.pop('name')
            models.PentestType.objects.get_or_create(name=name, defaults=item)

    def create_checklists(self):
        self.stdout.write('Creating checklists...')
        for data in self.data.get('checklist-categories', []):
            category_id = data.pop('id')
            items = data.pop('items')
            category, _created = Category.objects.get_or_create(category_id=category_id, defaults=data)
            for item in items:
                item_id = item.pop('id')
                Item.objects.get_or_create(item_id=item_id, category=category, defaults=item)
        for checklist in self.data.get('checklists', []):
            checklist_id = checklist.pop('id')
            categories = checklist.pop('categories')
            checklist, _created = Checklist.objects.get_or_create(checklist_id=checklist_id, defaults=checklist)
            for category_id in categories:
                try:
                    category = Category.objects.get(category_id=category_id)
                except Category.DoesNotExist:
                    continue
                checklist.categories.add(category)
            checklist.save()

    def create_companies(self):
        self.stdout.write('Creating sample companies...')
        for item in self.data.get('companies', []):
            name = item.pop('name')
            contacts = item.pop('contacts', [])
            item['report_template'] = models.ReportTemplate.objects.get(name='default_template')
            company, _created = models.Company.objects.get_or_create(name=name, defaults=item)
            for contact in contacts:
                models.CompanyContact.objects.get_or_create(company=company, first_name=contact['first_name'],
                                                            last_name=contact['last_name'], defaults=contact)

    def create_project_assets(self, project, data):
        for item in data:
            asset_type = item.pop('type')
            if asset_type == 'host':
                models.Host.objects.get_or_create(ip=item['ip'], project=project, defaults=item)
            elif asset_type == 'web_application':
                models.WebApplication.objects.get_or_create(base_url=item['base_url'], project=project, defaults=item)
            elif asset_type == 'thick_client':
                models.ThickClient.objects.get_or_create(name=item['name'], project=project, defaults=item)

    def create_projects(self):
        self.stdout.write('Creating sample projects...')
        for item in self.data.get('projects', []):
            name = item.pop('name')
            company_name = item.pop('company')
            members = item.pop('members', [])
            assets = item.pop('assets', [])
            item['test_method'] = TestMethod[item['test_method']]
            pentest_types = models.PentestType.objects.filter(name__in=item['pentest_types'])
            company = models.Company.objects.get(name=company_name)
            item.pop('pentest_types')
            project, _created = models.Project.objects.get_or_create(name=name, company=company, defaults=item)
            for pentest_type in pentest_types:
                project.pentest_types.add(pentest_type)
            project.save()
            for member in members:
                member['role'] = Roles[member['role']]
                username = member.pop('username')
                user = models.User.objects.get(username=username)
                models.Membership.objects.get_or_create(user=user, project=project, defaults=member)
            self.create_project_assets(project, assets)

    def create_technologies(self):
        self.stdout.write('Create sample technologies...')
        for item in self.data.get('technologies', []):
            name = item.pop('name')
            _tech, _created = models.Technology.objects.get_or_create(name=name, defaults={
                'homepage': item.get('homepage'),
                'cpe': item.get('cpe'),
                'description': item.get('description')
            })

    def create_attack_surface_data(self):
        if not self.data.get('attack-surface'):
            return
        self.stdout.write('Create Attack Surface Dashboard data...')
        for data in self.data.get('attack-surface', {}).get('tags', []):
            _tag, _created = asmonitor_models.Tag.objects.get_or_create(name=data['name'], defaults={
                'description': data['description'],
                'color': data['color']
            })

        for data in self.data['attack-surface'].get('programs', []):
            program, _created = asmonitor_models.Program.objects.get_or_create(name=data['name'], defaults={
                'description': data.get('description')
            })
            for target_data in data.get('targets', []):
                target, created = asmonitor_models.Target.objects.get_or_create(name=target_data['name'],
                                                                                ip=target_data['ip'],
                                                                                program=program)
                for tech_data in target_data.get('technologies', []):
                    tech, _created = models.Technology.objects.get_or_create(name=tech_data['name'], defaults={
                        'description': tech_data.get('description'),
                        'cpe': tech_data.get('cpe'), 'homepage': tech_data.get('homepage')
                    })
                    target.technologies.add(tech)
                for tag_data in target_data.get('tags', []):
                    tag, _created = asmonitor_models.Tag.objects.get_or_create(name=tag_data['name'], defaults={
                        'description': data.get('description'),
                        'color': data.get('color')
                    })
                    target.tags.add(tag)
                target.save()
                for finding_data in target_data.get('findings', []):
                    _finding, _created = asmonitor_models.Finding.objects.get_or_create(name=finding_data['name'],
                                                                                        program=program,
                                                                                        target=target, defaults={
                            'severity': Severity[finding_data['severity'].upper()].value,
                            'proof_text': finding_data['proof_text'],
                            'user': models.User.objects.get(username=finding_data['user'])
                        })
