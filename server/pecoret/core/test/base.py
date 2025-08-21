from ddf import G
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse_lazy

from advisories.models import advisory
from backend.models import (
    User, Project, Membership, Asset,
    Finding
)
from backend.models.api_token import APIToken, AccessChoices
from backend.models.membership import Roles
from checklists.models import (
    AssetChecklist
)
from core.storage.models import ImageFile


class PeCoReTTestCaseMixin:
    api_access_choices = AccessChoices

    def init_mixin(self):
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

        # assets
        self.asset1 = self.create_instance(Asset, project=self.project1)
        self.asset2 = self.create_instance(Asset, project=self.project2)
        self.init_advisory_users()

    def set_token_header(self, token):
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer " + token

    def init_advisory_users(self):
        self.advisory1 = self.create_instance(advisory.Advisory, report_template='default_template',
                                              user=self.pentester1)
        self.advisory2 = self.create_instance(advisory.Advisory, report_template='default_template',
                                              user=self.pentester2)

    def create_api_token(self, user, date_expire=None, **kwargs):
        return APIToken.objects.create_token(user=user, **kwargs)

    def api_token_check(self, user, scope, url, func, status_r, status_w, status_n, **kwargs):
        token_w, token_r, token_n = self.create_api_tokens_scope(user, scope=scope)
        self.set_token_header(token_n)
        self.basic_status_code_check(url, func, status_n, **kwargs)
        self.set_token_header(token_r)
        self.basic_status_code_check(url, func, status_r, **kwargs)
        self.set_token_header(token_w)
        self.basic_status_code_check(url, func, status_w, **kwargs)

    def create_api_tokens_scope(self, user, scope):
        """
        creates a set of API tokens for a given scope with all available permissions

        :param user:
        :param scope:
        :return:
        """
        _, token_r = self.create_api_token(user, **{scope: self.api_access_choices.READ})
        _, token_w = self.create_api_token(user, **{scope: self.api_access_choices.READ_WRITE})
        _, token_n = self.create_api_token(user, **{scope: self.api_access_choices.NO_ACCESS})
        return token_w, token_r, token_n

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
        return G(Project, company__report_template="default_template")

    def assign_project_role(self, user, role, project):
        return G(Membership, user=user, role=role, project=project)

    def get_url(self, endpoint, **kwargs):
        return reverse_lazy(endpoint, kwargs=kwargs)

    def create_instance(self, obj_class, **kwargs):
        return G(obj_class, **kwargs)

    def create_finding(self, **kwargs):
        return self.create_instance(Finding, **kwargs)

    def create_asset_checklist(self, **kwargs):
        return self.create_instance(AssetChecklist, **kwargs)

    def get_content_type_for_model(self, model):
        return ContentType.objects.get_for_model(model)

    def basic_status_code_check(self, url, req_func, status_code, data=None, debug=False, format="json", **kwargs):
        if data is None:
            response = req_func(url, **kwargs)
        else:
            response = req_func(url, data, format=format, **kwargs)
        if debug:
            print(response.json())
        self.assertEqual(response.status_code, status_code)
        return response

    def create_image_file(self, upload_directory, **kwargs):
        image_file = ImageFile(image=SimpleUploadedFile('test.jpg', b'test'), **kwargs)
        image_file.upload_directory = upload_directory
        image_file.save()
        return image_file
