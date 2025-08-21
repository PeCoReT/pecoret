from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from django.utils.translation import gettext as _
from django.conf import settings
from matplotlib.ticker import MaxNLocator

from backend import models
from backend.models import AssetType
from backend.models.vulnerability import Severity
from pecoret.reporting.components.chart import Chart
from pecoret.reporting.template import errors
from pecoret.reporting.template import mixins
from pecoret.reporting.template.base import GenericReportTemplate


class FindingBarChart(Chart):
    def __init__(self, findings):
        super().__init__()
        self.findings = findings
        origin = Path(__file__).parent
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Regular.ttf'))
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Bold.ttf'))
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Light.ttf'))
        mpl.rcParams['font.family'] = 'Roboto'
        mpl.rcParams['font.size'] = 9

    def plot(self):
        fig, ax = plt.subplots(figsize=[6, 2.5])
        findings = self.findings.exclude_fixed()
        labels = [_('Critical'), _('High'), _('Medium'), _('Low'), _('Informational')]
        counts = [
            findings.with_severity('critical').count(),
            findings.with_severity('high').count(),
            findings.with_severity('medium').count(),
            findings.with_severity('low').count(),
            findings.with_severity('informational').count()
        ]
        colors = [
            '#9c1720', '#d13c0f', '#e8971e', '#2075f5', '#059D1D', '#43616f'
        ]
        ax.bar(labels, counts, color=colors)
        ya = ax.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))
        return self.to_html(plt)


class ReportTemplate(mixins.SingleFindingMixin, mixins.AdvisoryMixin, mixins.PentestReportMixin,
                     mixins.AttackSurfaceFindingMixin,
                     GenericReportTemplate):
    css_files = []
    _error_classes = {
        'finding': [
            errors.FindingProofCheck
        ],
        'pentest_report': [
            errors.FindingProofCheck, errors.ExecutiveSummaryCheck, errors.VersionHistoryCheck
        ]
    }

    pentest_report_sections = [
        'cover.html', 'report_errors.html', 'toc.html', 'version_history.html', 'assessment_information.html',
        'executive_summary.html', 'technical_summary.html', 'technical_details.html', 'last_page.html'
    ]
    advisory_sections = [
        'advisory/cover.html', 'advisory/single.html'
    ]
    attack_surface_finding_sections = [
        'attack_surface/cover.html', 'attack_surface/single.html'
    ]

    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context['css_body_classes'] = ""
        context['is_draft'] = False
        if kwargs.get('report_document'):
            doc = kwargs['report_document']
            if doc.get_release_type_display() in ['Draft', 'Preview']:
                context['css_body_classes'] = 'draft'
                context['is_draft'] = True
        return context

    def get_single_finding_context(self, finding):
        context = super().get_single_finding_context(finding)
        self.check_errors('finding', context)
        # show report errors in single finding export
        context['report_errors'] = self.get_errors()
        return context

    def get_pentest_report_context(self, report_document):
        project = report_document.report.project
        context = super().get_pentest_report_context(report_document)
        findings = models.Finding.objects.for_report(project)
        vulnerabilities = models.ProjectVulnerability.objects.for_project(project).filter(
            pk__in=findings.values('vulnerability'))
        context['vulnerabilities'] = vulnerabilities
        context['findings'] = findings
        context['asset_types'] = AssetType.objects.all()
        context['settings'] = {
            'SITE_NAME': settings.SITE_NAME
        }
        context['scopes'] = models.ProjectScope.objects.for_project(project)
        context['members'] = models.Membership.objects.for_project(project).for_report()
        context['charts'] = {
            'findings_bar': FindingBarChart(findings)
        }
        if context.get('is_draft') is True:
            self.check_errors('pentest_report', context)
            context['report_errors'] = self.get_errors()
        return context

    def get_findings_count_for_asset(self, asset, severity=None):
        qs = asset.finding_set.exclude(exclude_from_report=True)
        if severity:
            qs = qs.filter(severity=Severity[severity].value)
        return qs.count()

    def get_asset_type_logo(self, asset_type):
        if asset_type.name == 'Web Application':
            return "web_application"
        elif asset_type.name == 'Mobile Application':
            return 'mobile_application'
        elif asset_type.name == 'Thick Client':
            return 'thick_client'
        return 'generic'
