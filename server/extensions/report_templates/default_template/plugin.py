from extra_settings.models import Setting
from backend import models
from backend.models.vulnerability import Severity
from pecoret.reporting import generators
from pecoret.reporting.report_plugin import BaseReportPlugin
from .charts import FindingBarChart
from .excel import ExcelGenerator
from .report_errors import ReportErrorMixin


class ReportPlugin(ReportErrorMixin, BaseReportPlugin):
    project_report_asset_classes = [
        models.Host, models.WebApplication,
        models.ThickClient, models.MobileApplication,
        models.GenericAsset
    ]
    SEVERITY_COLORS = {
        'critical': '#9c1720',
        'high': '#d13c0f',
        'medium': '#e8971e',
        'low': '#2075f5',
        'informational': '#059D1D',
        'fixed': ' #43616f'
    }
    css_files = [
        'css/main.css'
    ]

    def export_project_pdf_report(self, report_document):
        project = report_document.report.project
        findings = models.Finding.objects.for_report(project)
        self.project = project
        data = {
            'project': project,
            'report_document': report_document,
            'scopes': models.ProjectScope.objects.for_project(project),
            'version': self._get_report_document_version(report_document),
            'members': models.Membership.objects.for_project(project).for_report(),
            'findings': findings,
            'vulnerabilities': models.ProjectVulnerability.objects.for_project(project).filter(
                pk__in=findings.values('vulnerability')),
            'charts': {
                'findings_bar': FindingBarChart(findings, self.SEVERITY_COLORS),
            },
            'settings': {
                'GENERAL_COMPANY_NAME': Setting.get('GENERAL_COMPANY_NAME'),
            },
            'severity_colors': self.SEVERITY_COLORS
        }
        context = self.get_context(**data)
        context['report_errors'] = self.check_pdf_report_errors(context)
        generator = generators.PDFReportGenerator(self, context, language=project.language)
        return generator.generate('pentest_report.html')

    def export_project_excel(self, report_document):
        context = self.get_context(**{
            'findings': models.Finding.objects.for_report(report_document.report.project)
        })
        generator = ExcelGenerator(self, context)
        return generator.generate(None)

    def export_vulnerability_csv(self, report_document):
        context = self.get_context(**{
            'findings': models.Finding.objects.for_report(report_document.report.project)
        })
        generator = generators.CSVGenerator(self, context)
        return generator.generate('vulnerability_overview.csv')

    def export_single_finding(self, finding):
        context = self.get_context(**{
            'finding': finding, 'project': finding.project,
            'severity_colors': self.SEVERITY_COLORS
        })
        context['report_errors'] = self.check_pdf_report_errors(context)
        generator = generators.PDFReportGenerator(self, context, language=finding.project.language)
        return generator.generate('single_finding_export.html')

    def export_advisory_pdf(self, advisory):
        context = self.get_context(**{'advisory': advisory, 'severity_colors': self.SEVERITY_COLORS})
        generator = generators.PDFReportGenerator(self, context)
        return generator.generate('advisory_export.html')

    def _get_report_document_version(self, report_document):
        qs = models.ChangeHistory.objects.filter(report=report_document.report)
        if qs.exists():
            return qs.order_by('-version').first()
        return '0.1'

    def get_findings_count_for_asset(self, asset, severity=None):
        qs = asset.findings.exclude(exclude_from_report=True)
        if severity:
            qs = qs.filter(severity=Severity[severity].value)
        return qs.count()

    def get_assets(self):
        assets = []
        for asset_class in self.project_report_asset_classes:
            assets += list(asset_class.objects.for_project(self.project))
        return assets

    def on_preprocess(self, generator, **kwargs):
        if isinstance(generator, generators.PDFReportGenerator):
            generator.css_files += self.css_files
