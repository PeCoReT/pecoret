from ddf import G
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from extra_settings.models import Setting

from backend.models import (
    User, Project, Membership, ReportTemplate, WebApplication,
    Finding
)
from backend.models import advisory
from backend.models.advisory_membership import AdvisoryMembership
from backend.models.api_token import APIToken, AccessChoices
from backend.models.membership import Roles
from checklists.models import (
    AssetChecklist
)


class PeCoReTTestCaseMixin:
    api_access_choices = AccessChoices

    def init_mixin(self):
        Setting.set_defaults_from_settings()
        self.pentester1 = self.create_user("pentester1", "changeme", group="Pentester")
        self.project1 = self.create_project()
        self.assign_project_role(self.pentester1, Roles.CONTRIBUTOR, self.project1)
        # create second project
        self.pentester2 = self.create_user("pentester2", "changeme", group="Pentester")
        self.project2 = self.create_project()
        self.assign_project_role(self.pentester2, Roles.CONTRIBUTOR, self.project2)
        # read only
        self.read_only1 = self.create_user("readonly1", "changeme", group="Pentester")
        self.assign_project_role(self.read_only1, Roles.READ_ONLY, self.project1)
        # management
        self.management1 = self.create_user("management1", "changeme", group="Management")
        self.assign_project_role(self.management1, Roles.OWNER, self.project1)
        self.management2 = self.create_user("management2", "changeme", group="Management")
        self.assign_project_role(self.management2, Roles.OWNER, self.project2)
        # non-grouped user
        self.user1 = self.create_user("user1", "changeme")
        # customer
        self.customer1 = self.create_user('customer1', 'changeme', group='Customer')
        self.customer1.company = self.project1.company
        self.customer1.save()
        self.customer2 = self.create_user('customer2', 'changeme', group='Customer')
        self.customer2.company = self.project2.company
        self.customer2.save()

        # superuser
        self.superuser = self.create_user("superuser", "changeme", is_superuser=True, is_staff=True)

        self.advisory_manager1 = self.create_user("advisory1", "changeme", group="Advisory Management")

        # assets
        self.asset1 = self.create_instance(WebApplication, project=self.project1)
        self.asset2 = self.create_instance(WebApplication, project=self.project2)
        self.init_advisory_users()

    def set_token_header(self, token):
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer " + token

    def init_advisory_users(self):
        self.vendor1 = self.create_user("testvendor1", "changeme1234", group="Vendor")
        self.read_only_vendor = self.create_user("readonlyvendor1", "changeme1234", group="Vendor")
        self.vendor2 = self.create_user("testvendor2", "changeme1234", group="Vendor")
        self.advisory1 = self.create_instance(advisory.Advisory, visibility=advisory.VisibilityChoices.TEAM,
                                              user=self.pentester1)
        self.advisory2 = self.create_instance(advisory.Advisory, visibility=advisory.VisibilityChoices.MEMBERS,
                                              user=self.pentester2)
        self.assign_advisory_role(self.vendor1, advisory.Roles.VENDOR, self.advisory1)
        self.assign_advisory_role(self.read_only_vendor, advisory.Roles.READ_ONLY, self.advisory1)

    def create_api_token(self, user, **kwargs):
        return APIToken.objects.create_token(user=user, **kwargs)

    def assign_advisory_role(self, user, role, advisory):
        return G(AdvisoryMembership, user=user, role=role, advisory=advisory)

    def create_user(self, username, password, is_staff=False, group=None, **kwargs):
        email = "%s@example.com" % username
        user = User.objects.create_user(username, password=password, is_staff=is_staff, email=email, **kwargs)
        if group:
            user.groups.add(Group.objects.get(name=group))
            user.save()
        return user

    def add_user_to_group(self, user, group_name):
        user.groups.add(Group.objects.get(name=group_name))
        user.save()

    def create_project(self):
        return G(Project, company__report_template=ReportTemplate.objects.get(name="default_template"))

    def assign_project_role(self, user, role, project):
        return G(Membership, user=user, role=role, project=project)

    def get_url(self, endpoint, **kwargs):
        return reverse_lazy(endpoint, kwargs=kwargs)

    def create_instance(self, obj_class, **kwargs):
        return G(obj_class, **kwargs)

    def create_finding(self, **kwargs):
        kwargs["component_object_id"] = kwargs["component"].pk
        kwargs["component_content_type"] = self.get_content_type_for_model(kwargs["component"])
        return self.create_instance(Finding, **kwargs)

    def create_asset_checklist(self, **kwargs):
        kwargs["component_object_id"] = kwargs["component"].pk
        kwargs["component_content_type"] = self.get_content_type_for_model(kwargs["component"])
        return self.create_instance(AssetChecklist, **kwargs)

    def get_content_type_for_model(self, model):
        return ContentType.objects.get_for_model(model)

    def basic_permission_checks(self, url, user_status_map, req_func, data=None, debug=False):
        for u in user_status_map:
            user = u[0]
            status_code = u[1]
            self.client.force_login(user)
            if data is None:
                response = req_func(url)
            else:
                response = req_func(url, data)
            if debug:
                print(response.json())
            self.assertEqual(response.status_code, status_code, msg="Usermap: %s" % str(u))

    def basic_status_code_check(self, url, req_func, status_code, data=None, debug=False, format="json"):
        if data is None:
            response = req_func(url)
        else:
            response = req_func(url, data, format=format)
        if debug:
            print(response.json())
        self.assertEqual(response.status_code, status_code)
        return response
