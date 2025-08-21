from attack_surface.models import Program, Scope, ScopeItem, ScopeItemCategory, Target
from attack_surface.models.scoping.item import ScopeResult
from pecoret.core.test import PeCoReTTestCaseMixin


class AttackSurfaceMixin(PeCoReTTestCaseMixin):
    def init_mixin(self):
        super().init_mixin()
        self.initialize_attack_surface_data()

    def initialize_attack_surface_data(self):
        self.program1 = self.create_instance(Program)
        self.program2 = self.create_instance(Program)

        self.scope1 = self.create_instance(Scope, program=self.program1)
        self.scope2 = self.create_instance(Scope, program=self.program2)

        ScopeItem.objects.create(scope=self.scope1, value="example10.com", category=ScopeItemCategory.DOMAIN,
                                 results_in=ScopeResult.INCLUDE)
        ScopeItem.objects.create(scope=self.scope1, value="example11.com", category=ScopeItemCategory.DOMAIN,
                                 results_in=ScopeResult.INCLUDE)

        self.target1 = self.create_instance(Target, program=self.program1, data="example10.com")
        self.target11 = self.create_instance(Target, program=self.program1, data="aa.example10.com")

        self.target2 = self.create_instance(Target, program=self.program1, data="example11.com")
        self.target3 = self.create_instance(Target, program=self.program2, data="example20.com")
        self.target4 = self.create_instance(Target, program=self.program2, data="example21.com")

    def set_scanner_token(self, token):
        self.client.defaults["X-Scanner-Auth"] = token
