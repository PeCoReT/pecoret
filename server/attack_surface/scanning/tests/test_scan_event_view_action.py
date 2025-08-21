from datetime import timedelta

from rest_framework.test import APITestCase

from attack_surface.models import Scanner, URL, Target, Service, Program, ScopeItem
from attack_surface.models.scoping.item import ScopeResult, ScopeItemCategory
from attack_surface.scanning.models import ScanBatchRequest, ScanTemplate
from attack_surface.scanning.scheduler.scan_event import fuzzy_guess_target_program
from attack_surface.tests.mixin import AttackSurfaceMixin


class ScannerSubmitResultTest(AttackSurfaceMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.program = self.create_instance(Program)
        self.template = self.create_instance(
            ScanTemplate, cooldown=timedelta(minutes=0)
        )
        self.scanner = self.create_instance(Scanner)
        self.batch = self.create_instance(ScanBatchRequest, scan_template=self.template)
        self.url = self.get_url(
            "api:attack_surface:scan-request-result", pk=self.batch.pk
        )
        self.headers = {"X-Scanner-Auth": self.scanner.token}

    def test_submit_discovery_url(self):
        payload = {
            "url": "http://discovered.example.com:8080/path",
            "service": {"banner": "nginx"},
        }
        data = {
            "event_type": "discovery.url",
            "payload": payload,
            "raw_line": "Found http://discovered.example.com:8080/path",
        }

        response = self.client.post(self.url, data, format="json", headers=self.headers)
        self.assertEqual(response.status_code, 200)

        # Ensure raw_line is appended to raw_output
        # self.batch.refresh_from_db()
        # self.assertIn(
        #    "Found http://discovered.example.com:8080/path", self.batch.raw_output
        # )

        # URL, Target, and Service should now exist
        self.assertTrue(
            URL.objects.filter(url="http://discovered.example.com:8080/path").exists()
        )
        self.assertTrue(Target.objects.filter(data="discovered.example.com").exists())
        self.assertTrue(Service.objects.filter(port_number=8080).exists())

    def test_unauthorized(self):
        # Should reject without scanner auth
        data = {
            "event_type": "discovery.url",
            "payload": {"url": "http://unauth.test"},
            "raw_line": "unauthorized line",
        }
        response = self.client.post(self.url, data, format="json")  # no headers
        self.assertEqual(response.status_code, 403)

    def test_fuzzy_guess_target_program_from_scope_include(self):
        program = self.create_instance(Program)
        self.create_instance(
            ScopeItem,
            value="example.com",
            scope__program=program,
            category=ScopeItemCategory.DOMAIN,
            results_in=ScopeResult.INCLUDE,
        )

        guessed_program = fuzzy_guess_target_program("sub.example.com")
        self.assertEqual(guessed_program, program)

    def test_fuzzy_guess_target_program_from_existing_target(self):
        program = self.create_instance(Program)
        self.create_instance(Target, data="sub.example.com", program=program)

        guessed_program = fuzzy_guess_target_program("sub.example.com")
        self.assertEqual(guessed_program, program)

    def test_fuzzy_guess_target_program_from_scope_exclude(self):
        program = self.create_instance(Program)
        self.create_instance(
            ScopeItem,
            value="example.com",
            scope__program=program,
            category=ScopeItemCategory.DOMAIN,
            results_in=ScopeResult.EXCLUDE,
        )

        guessed_program = fuzzy_guess_target_program("sub.example.com")
        self.assertEqual(guessed_program, program)

    def test_fuzzy_guess_target_program_returns_none(self):
        guessed_program = fuzzy_guess_target_program("unknown.io")
        self.assertIsNone(guessed_program)

    def test_submit_discovery_url_bulk(self):
        payload = [
            {
                "url": "http://bulk1.example.com:8000/page",
                "service": {"banner": "apache"},
                "technologies": ["cpe:2.3:a:apache:http_server"],
                "tags": ["webserver"],
            },
            {
                "url": "https://bulk2.example.com/page2",
                "service": {"banner": "nginx"},
                "technologies": ["cpe:2.3:a:nginx:nginx"],
                "tags": ["reverse-proxy", "webserver"],
            },
        ]
        data = {
            "event_type": "discovery.url-bulk",
            "bulk": payload,
            "raw_line": "Bulk discovered urls",
        }

        response = self.client.post(self.url, data, format="json", headers=self.headers)
        self.assertEqual(response.status_code, 200)

        # Validate both URLs created
        self.assertTrue(
            URL.objects.filter(url="http://bulk1.example.com:8000/page").exists()
        )
        self.assertTrue(
            URL.objects.filter(url="https://bulk2.example.com/page2").exists()
        )

        url1 = URL.objects.get(url="http://bulk1.example.com:8000/page")
        url2 = URL.objects.get(url="https://bulk2.example.com/page2")

        # Validate technologies and tags set
        self.assertTrue(
            url1.technologies.filter(name="cpe:2.3:a:apache:http_server").exists()
        )
        self.assertTrue(url2.technologies.filter(name="cpe:2.3:a:nginx:nginx").exists())
        self.assertTrue(url1.tags.filter(name="webserver").exists())
        self.assertTrue(url2.tags.filter(name="reverse-proxy").exists())
        self.assertTrue(url2.tags.filter(name="webserver").exists())

    def test_event_result_uses_scope_include_program(self):
        program = self.create_instance(Program, name="Test Program")
        self.create_instance(
            ScopeItem,
            value="example.com",
            scope__program=program,
            category=ScopeItemCategory.DOMAIN,
            results_in=ScopeResult.INCLUDE,
        )
        scan_batch = self.create_instance(
            ScanBatchRequest, scan_template__cooldown=timedelta(minutes=0)
        )

        headers = {"X-Scanner-Auth": self.scanner.token}
        payload = {
            "event_type": "discovery.url",
            "payload": {"url": "http://sub.example.com/page", "service": {}},
            "raw_line": "discovered http://sub.example.com/page",
        }

        url = self.get_url("api:attack_surface:scan-request-result", pk=scan_batch.pk)
        response = self.client.post(url, data=payload, format="json", headers=headers)
        self.assertEqual(response.status_code, 200)

        # Verify the target was created under the correct program
        target = Target.objects.get(data="sub.example.com")
        self.assertEqual(target.program, program)

        # And that the URL exists
        self.assertTrue(URL.objects.filter(url="http://sub.example.com/page").exists())

    def test_submit_discovery_url_with_technologies(self):
        payload = {
            "url": "http://tech.example.com",
            "service": {"banner": "Apache"},
            "technologies": ["Django", "PostgreSQL"],
        }
        data = {
            "event_type": "discovery.url",
            "payload": payload,
            "raw_line": "Found http://tech.example.com",
        }

        response = self.client.post(self.url, data, format="json", headers=self.headers)
        self.assertEqual(response.status_code, 200)

        url_obj = URL.objects.get(url="http://tech.example.com")
        tech_names = list(url_obj.technologies.values_list("name", flat=True))
        self.assertCountEqual(tech_names, ["Django", "PostgreSQL"])

    def test_error_filled(self):
        data = {"event_type": "batch.finished", "output": "test123"}
        response = self.client.post(self.url, data, format="json", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        b = ScanBatchRequest.objects.filter(
            pk=self.batch.pk, raw_output__contains="test123"
        )
        self.assertEqual(b.count(), 1)

    def test_submit_discovery_url_with_tags(self):
        payload = {
            "url": "http://tagged.example.com",
            "service": {"banner": "Caddy"},
            "tags": ["Production", "Internal"],
        }
        data = {
            "event_type": "discovery.url",
            "payload": payload,
            "raw_line": "Found http://tagged.example.com",
        }

        response = self.client.post(self.url, data, format="json", headers=self.headers)
        self.assertEqual(response.status_code, 200)

        url_obj = URL.objects.get(url="http://tagged.example.com")
        tag_names = list(url_obj.tags.values_list("name", flat=True))
        self.assertCountEqual(tag_names, ["Production", "Internal"])
