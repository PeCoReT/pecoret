from django.conf import settings
from rest_framework.test import APITestCase
from django_q.tasks import async_task, result
from backend import models
from backend.models.reports.report_release import ReleaseType
from backend.tasks.reporting import create_report_document_task
from backend.tasks.reporting import export_single_finding
from pecoret.core.test import PeCoReTTestCaseMixin


class ReportGenerationTask(APITestCase, PeCoReTTestCaseMixin):
    """test if report is compiled successfully"""

    def setUp(self) -> None:
        self.init_mixin()
        self.report_template = list(settings.REPORT_TEMPLATES.keys())[0]
        self.report = self.create_instance(
            models.Report, project=self.project1, template=self.report_template
        )
        self.report_document = self.create_instance(
            models.ReportRelease, report=self.report, release_type=ReleaseType.DRAFT
        )
        self.create_instance(models.ChangeHistory, report=self.report)
        self.create_instance(
            models.Finding,
            project=self.project1,
            vulnerability__project=self.project1,
            asset=self.asset1,
            user=self.pentester1,
        )

    def test_report_generation_task(self):
        task_id = async_task(
            create_report_document_task, self.report_document.pk, sync=True
        )
        task_result = result(task_id, 200)
        self.assertIsNotNone(task_result)
        self.assertEqual(
            models.ReportRelease.objects.filter(compiled_source__isnull=False).count(),
            1,
        )

    def test_report_generation_task_german(self):
        self.report.project.language = "de"
        task_id = async_task(
            create_report_document_task, self.report_document.pk, sync=True
        )
        task_result = result(task_id, 200)
        self.assertIsNotNone(task_result)
        self.assertEqual(
            models.ReportRelease.objects.filter(compiled_source__isnull=False).count(),
            1,
        )

    def test_non_draft_report(self):
        self.report_document.release_type = ReleaseType.FINAL
        task_id = async_task(create_report_document_task, self.report_document.pk, sync=True)
        task_result = result(task_id, 200)
        self.assertIsNotNone(task_result)
        self.assertEqual(
            models.ReportRelease.objects.filter(compiled_source__isnull=False).count(),
            1,
        )

    def test_non_existent_template(self):
        # TODO: implement
        pass


class SingleFindingExportTask(APITestCase, PeCoReTTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.finding = self.create_instance(
            models.Finding,
            project=self.project1,
            vulnerability__project=self.project1,
            asset=self.asset1,
            user=self.pentester1,
        )

    def test_finding_export_task(self):
        task_id = async_task(
            export_single_finding, self.finding, "default_template", sync=True
        )
        task_result = result(task_id, 200)
        self.assertIsNotNone(task_result)
