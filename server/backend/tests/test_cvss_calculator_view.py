from rest_framework.test import APITestCase
from pecoret.core.test import PeCoReTTestCaseMixin


class CVSS31CalculatorViewTestCase(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.url = self.get_url("api:backend:cvss31-calculator")

    def test_calculate(self):
        self.client.force_login(self.pentester1)
        data = {
            'vector': 'CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:L/A:H'
        }
        response = self.basic_status_code_check(self.url, self.client.post, 200, data=data)
        self.assertEqual(response.json()['score'], 6.7)
        self.assertEqual(response.json()['severity'], 'Medium')
