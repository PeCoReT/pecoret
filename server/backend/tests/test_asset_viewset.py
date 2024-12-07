from rest_framework.test import APITestCase

from backend.models import AssetType, CustomFieldAsset, CustomFieldAssetValue
from backend.models.asset import Asset, Environment, AssetAccessibility
from pecoret.core.test import PeCoReTTestCaseMixin


class AssetListViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.asset1 = self.create_instance(Asset, project=self.project1)
        self.asset2 = self.create_instance(Asset, project=self.project2)
        self.url = self.get_url("api:backend:asset-list", project=self.project1.pk)
        self.allowed_users = [
            self.pentester1, self.management1, self.read_only1
        ]
        self.forbidden_users = [
            self.pentester2, self.management2, self.user1, self.customer1, self.customer2
        ]

    def test_status_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)


class AssetCreateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:asset-list", project=self.project1.pk)
        self.asset_type = self.create_instance(AssetType)
        self.asset_type2 = self.create_instance(AssetType)
        self.data = {"name": "testcreateview", "asset_type": self.asset_type.pk,
                     "environment": Environment.UNKNOWN.label, "accessible": AssetAccessibility.UNKNOWN.label}

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)

    def test_status_forbidden(self):
        users = [
            self.pentester2, self.management2, self.user1, self.read_only1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.post, 403, data=self.data)

    def test_custom_field_create(self):
        # test if fields are validated correctly and are required for this asset type
        self.custom_field = self.create_instance(CustomFieldAsset,
                                                 name="testcreatefield",
                                                 field_type=CustomFieldAsset.get_field_type_choices().URL)
        self.custom_field.asset_types.add(self.asset_type)
        self.custom_field.save()
        self.data["custom_testcreatefield"] = "invalidurl"
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.post, 400, data=self.data)
        self.data["custom_testcreatefield"] = "http://127.0.0.1"
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        asset = Asset.objects.get(name="testcreateview")
        asset_value = CustomFieldAssetValue.objects.get(asset=asset, field=self.custom_field)
        self.assertEqual(asset_value.value, "http://127.0.0.1")

    def test_custom_field_asset_type(self):
        # test with invalid asset type validation, so no fields are set, when not configured for this asset type
        self.custom_field = self.create_instance(CustomFieldAsset,
                                                 name="testcreatefield",
                                                 field_type=CustomFieldAsset.get_field_type_choices().URL)
        self.custom_field.asset_types.clear()
        self.client.force_login(self.pentester1)
        self.data["custom_testcreatefield"] = "http://127.0.0.1"
        self.basic_status_code_check(self.url, self.client.post, 201, data=self.data)
        custom_field = CustomFieldAssetValue.objects.filter(field=self.custom_field)
        self.assertEqual(len(custom_field), 0)


class AssetUpdateViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.asset1 = self.create_instance(Asset, project=self.project1)
        self.asset2 = self.create_instance(Asset, project=self.project2)
        self.url = self.get_url("api:backend:asset-detail", project=self.project1.pk,
                                pk=self.asset1.pk)
        self.data = {"name": "newname"}

    def test_allowed(self):
        users = [
            self.management1, self.pentester1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_forbidden(self):
        users = [
            self.management2, self.pentester2, self.read_only1, self.user1
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_broken_access(self):
        url = self.get_url("api:backend:asset-detail", project=self.project2.pk, pk=self.asset1.pk)
        self.client.force_login(self.pentester2)
        response = self.client.patch(url, self.data, format="json")
        self.assertEqual(response.status_code, 404)

        url = self.get_url("api:backend:asset-detail", project=self.project1.pk, pk=self.asset2.pk)
        self.client.force_login(self.pentester2)
        response = self.client.patch(url, self.data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_custom_field_update(self):
        self.custom_field = self.create_instance(CustomFieldAsset,
                                                 name="testupdatefield",
                                                 field_type=CustomFieldAsset.get_field_type_choices().URL)
        self.custom_field.asset_types.add(self.asset1.asset_type)
        self.custom_field.save()
        self.data["custom_testupdatefield"] = "invalidurl"
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.patch, 400, data=self.data)
        self.data["custom_testupdatefield"] = "http://127.0.0.1"
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
        asset_value = CustomFieldAssetValue.objects.get(asset=self.asset1, field=self.custom_field)
        self.assertEqual(asset_value.value, "http://127.0.0.1")

    def test_custom_field_asset_type(self):
        # test with invalid asset type validation, so no fields are set, when not configured for this asset type
        self.custom_field = self.create_instance(CustomFieldAsset,
                                                 name="testcreatefield",
                                                 field_type=CustomFieldAsset.get_field_type_choices().URL)
        self.custom_field.asset_types.clear()
        self.client.force_login(self.pentester1)
        self.data["custom_testcreatefield"] = "http://127.0.0.1"
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)
        custom_field = CustomFieldAssetValue.objects.filter(field=self.custom_field)
        self.assertEqual(len(custom_field), 0)



class AssetDeleteViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.asset1 = self.create_instance(Asset, project=self.project1)
        self.url = self.get_url("api:backend:asset-detail", project=self.project1.pk,
                                pk=self.asset1.pk)

    def test_pentester1(self):
        self.client.force_login(self.pentester1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_management1(self):
        self.client.force_login(self.management1)
        self.basic_status_code_check(self.url, self.client.delete, 204)

    def test_forbidden(self):
        users = [
            self.read_only1, self.management2, self.user1, self.pentester2
        ]
        for user in users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.delete, 403)


class APITokenReadTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.token1, self.key1 = self.create_api_token(self.pentester1, scope_all_projects=self.api_access_choices.READ,
                                                       date_expire=None)
        self.token2, self.key2 = self.create_api_token(self.pentester1,
                                                       scope_all_projects=self.api_access_choices.NO_ACCESS,
                                                       date_expire=None)
        self.token3, self.key3 = self.create_api_token(self.pentester2,
                                                       scope_all_projects=self.api_access_choices.READ,
                                                       date_expire=None)
        self.web_application1 = self.create_instance(Asset, project=self.project1)
        self.url = self.get_url("api:backend:asset-detail", project=self.project1.pk,
                                pk=self.web_application1.pk)

    def test_valid(self):
        self.set_token_header(self.key1)
        self.basic_status_code_check(self.url, self.client.get, 200)

    def test_invalid(self):
        self.set_token_header(self.key2)
        self.basic_status_code_check(self.url, self.client.get, 403)

    def test_forbidden(self):
        self.set_token_header(self.key3)
        self.basic_status_code_check(self.url, self.client.get, 403)


class APITokenWriteTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.token1, self.key1 = self.create_api_token(self.pentester1, scope_all_projects=self.api_access_choices.READ,
                                                       date_expire=None)
        self.token2, self.key2 = self.create_api_token(self.pentester1,
                                                       scope_all_projects=self.api_access_choices.NO_ACCESS,
                                                       date_expire=None)
        self.token3, self.key3 = self.create_api_token(self.pentester2,
                                                       scope_all_projects=self.api_access_choices.READ,
                                                       date_expire=None)
        self.web_application1 = self.create_instance(Asset, project=self.project1)
        self.url = self.get_url("api:backend:asset-detail", project=self.project1.pk,
                                pk=self.web_application1.pk)
        self.data = {"name": "test123"}

    def test_valid(self):
        self.set_token_header(self.key1)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_read_write(self):
        self.token1.scope_all_projects = self.api_access_choices.READ_WRITE
        self.token1.save()
        self.set_token_header(self.key1)
        self.basic_status_code_check(self.url, self.client.patch, 200, data=self.data)

    def test_invalid(self):
        self.set_token_header(self.key2)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)

    def test_forbidden(self):
        self.set_token_header(self.key3)
        self.basic_status_code_check(self.url, self.client.patch, 403, data=self.data)


class CustomFieldAssetViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("api:backend:custom-field-asset-list")
        self.allowed_users = [
            self.pentester1, self.management1, self.read_only1, self.management2, self.pentester2
        ]
        self.forbidden_users = [
            self.user1, self.customer1, self.customer2
        ]

    def test_status_allowed(self):
        for user in self.allowed_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 200)

    def test_forbidden(self):
        for user in self.forbidden_users:
            self.client.force_login(user)
            self.basic_status_code_check(self.url, self.client.get, 403)
