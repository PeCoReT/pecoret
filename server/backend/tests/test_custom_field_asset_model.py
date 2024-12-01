from rest_framework.test import APITestCase
from rest_framework.validators import ValidationError

from backend.models import CustomFieldAsset, CustomFieldAssetValue, Asset
from core.custom_fields.models import FieldTypeChoices
from pecoret.core.test import PeCoReTTestCaseMixin


class CustomFieldAssetValidation(PeCoReTTestCaseMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.asset = self.create_instance(Asset)

    def test_validate_url_field(self):
        asset_url = self.create_instance(CustomFieldAsset, field_type=FieldTypeChoices.URL)
        self.assertRaises(ValidationError,
                          lambda: CustomFieldAssetValue.objects.create(field=asset_url, value="test111",
                                                                       asset=self.asset))

    def test_required_attribute(self):
        asset_char = self.create_instance(CustomFieldAsset, field_type=FieldTypeChoices.CHAR, required=True)
        self.assertRaises(ValidationError,
                          lambda: CustomFieldAssetValue.objects.create(field=asset_char, value=None, asset=self.asset)
                          )
        CustomFieldAssetValue.objects.create(field=asset_char, value="test", asset=self.asset)
