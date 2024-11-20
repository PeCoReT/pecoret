from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from core.storage.models import ImageFile
from pecoret.core.test import PeCoReTTestCaseMixin


class TestExternalAccessImages(PeCoReTTestCaseMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.image_file = self.create_image_file('attack_surface')
        self.url = self.get_url('api:backend:render-markdown')
        self.forbidden_users = [
            self.customer1, self.customer2, self.user1
        ]
        self.allowed_users = [
            self.pentester1, self.pentester2, self.read_only1, self.management2, self.management1
        ]

    def test_not_allowed_dir(self):
        self.image_file = self.create_image_file('projects')
        name = self.image_file.image.name
        test_string = f'this is a test string\n![caption](storage:///{name})'
        self.client.force_login(self.allowed_users[0])
        data = {'markdown': test_string}
        response = self.client.post(self.url, data)
        self.assertNotContains(response, 'data:')


    def test_render_storage_links_forbidden(self):
        """ test if external users get rendered storage links """
        name = self.image_file.image.name
        test_string = f'this is a test string\n![caption](storage:///{name})'
        data = {'markdown': test_string}
        for user in self.forbidden_users:
            self.client.force_login(user)
            response = self.client.post(self.url, data)
            self.assertNotContains(response, 'src=')
            self.assertNotContains(response, 'data')

    def test_render_storage_links_allowed(self):
        """ test if external users get rendered storage links """
        name = self.image_file.image.name
        test_string = f'this is a test string\n![caption](storage:///{name})'
        data = {'markdown': test_string}
        for user in self.allowed_users:
            self.client.force_login(user)
            response = self.client.post(self.url, data)
            self.assertContains(response, 'src=')
            self.assertContains(response, 'figure')
