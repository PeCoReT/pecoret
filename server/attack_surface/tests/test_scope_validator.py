from rest_framework.test import APITestCase

from attack_surface.models import Program, Target, Scope, ScopeItem, ScopeItemCategory
from attack_surface.models.scoping.item import ScopeResult
from attack_surface.models.target import ScopeChoices
from attack_surface.utils.scoping import check_target_scope
from pecoret.core.test import PeCoReTTestCaseMixin


class ScopeValidatorTests(PeCoReTTestCaseMixin, APITestCase):

    def setUp(self):
        self.program = self.create_instance(Program)
        self.scope = self.create_instance(Scope, program=self.program)
        self.create_instance(
            ScopeItem, scope=self.scope, category=ScopeItemCategory.DOMAIN,
            value="example.com", results_in=ScopeResult.INCLUDE
        )
        self.create_instance(
            ScopeItem, scope=self.scope, category=ScopeItemCategory.DOMAIN,
            value="example.net", results_in=ScopeResult.EXCLUDE
        )

    def test_scope_validator(self):
        scope = check_target_scope(Target.objects.create(data="example.com", program=self.program))
        self.assertEqual(scope, ScopeChoices.IN_SCOPE)

        scope = check_target_scope(Target.objects.create(data="examplea.com", program=self.program))
        self.assertEqual(scope, ScopeChoices.UNDEFINED)

        scope = check_target_scope(Target.objects.create(data="example.net", program=self.program))
        self.assertEqual(scope, ScopeChoices.OUT_OF_SCOPE)
        scope = check_target_scope(Target.objects.create(data="foo.example.net", program=self.program))
        self.assertEqual(scope, ScopeChoices.OUT_OF_SCOPE)

        scope = check_target_scope(Target.objects.create(data="foo-example.com", program=self.program))
        self.assertEqual(scope, ScopeChoices.UNDEFINED)

