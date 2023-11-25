import datetime
from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from django.conf import settings
from django.db.models import Count, Max, Q
from django.utils.translation import gettext as _
from matplotlib.ticker import MaxNLocator

from backend.models import ProjectVulnerability, Finding, Host, WebApplication, Membership, ProjectScope, Settings
from backend.models.project import ScoreChoices
from backend.models.vulnerability import Severity
from pecoret.core.reporting import types as report_types
from pecoret.core.reporting.charts.base import Chart
from pecoret.core.reporting.error import ReportError

SEVERITY_COLORS = {
    'critical': '#9c1720',
    'high': '#d13c0f',
    'medium': '#e8971e',
    'low': '#2075f5',
    'informational': '#059D1D',
    'fixed': ' #43616f'
}


class ErrorMixin:
    def check_finding_errors(self):
        # check finding errors
        for finding in Finding.objects.for_report(self.get_project()):
            if not finding.proof_text:
                error = ReportError("Missing proof!", f"#finding-{finding.pk}-proofs")
                self._add_error(error)
            if self.get_project().require_cvss_score is not None:
                score = ScoreChoices(self.get_project().require_cvss_score)
                if score == ScoreChoices['CVSS31_BASE']:
                    if finding.cvssbasescore.is_incomplete:
                        error = ReportError(
                            "Missing CVSS base score", f"#finding-{finding.pk}-title")
                        self._add_error(error)
                elif score == ScoreChoices['CVSS4_BASE']:
                    if not finding.cvss_score_40:
                        error = ReportError(
                            "Missing CVSS base score", f"#finding-{finding.pk}-title")
                        self._add_error(error)


class FindingBarChart(Chart):
    def __init__(self, findings):
        super().__init__()
        self.findings = findings

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
        colors = [SEVERITY_COLORS['critical'], SEVERITY_COLORS['high'], SEVERITY_COLORS['medium'],
                  SEVERITY_COLORS['low'], SEVERITY_COLORS['informational']]
        ax.bar(labels, counts, color=colors)
        ya = ax.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))
        return self.to_html(plt)


class PentestPDFReport(ErrorMixin, report_types.PentestPDFReport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        origin = Path(__file__).parent
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Regular.ttf'))
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Bold.ttf'))
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Light.ttf'))
        mpl.rcParams['font.family'] = 'Roboto'
        mpl.rcParams['font.size'] = 9

    def get_assets(self):
        assets = []
        assets += list(Host.objects.for_project(self.get_project()))
        assets += list(WebApplication.objects.for_project(self.get_project()))
        return assets

    def get_context(self):
        context = super().get_context()
        context["now"] = datetime.datetime.now().strftime("%B %d, %Y")
        context['settings'] = dict(Settings.objects.values()[0])
        context["REPORT_COMPANY_INFORMATION"] = settings.REPORT_COMPANY_INFORMATION
        context["findings"] = Finding.objects.for_report(self.get_project())
        context["members"] = Membership.objects.for_project(self.get_project()).for_report()
        context['vulnerabilities'] = ProjectVulnerability.objects.for_project(self.get_project()).filter(
            pk__in=context['findings'].values('vulnerability'))
        context["scopes"] = ProjectScope.objects.for_project(self.get_project())
        context["charts"] = {
            'findings_bar': FindingBarChart(context['findings']),
        }
        return context

    def get_unique_vulnerabilities_by_severity(self):
        return (
            ProjectVulnerability.objects.for_project(project=self.get_project())
            .annotate(
                count=Count(
                    "finding__pk", distinct=True, filter=~Q(exclude_from_report=True)
                )
            )
            .annotate(finding_severity=Max("finding__severity"))
            .order_by("-finding__severity", "vulnerability_id")
            .filter(count__gt=0)
        )

    def get_vulnerabilities(self):
        return ProjectVulnerability.objects.for_project(
            project=self.get_project()
        ).filter(finding__is_null=False)

    def get_findings_count_for_asset(self, asset, severity=None):
        qs = asset.findings.exclude(exclude_from_report=True)
        if severity:
            qs = qs.filter(severity=Severity[severity].value)
        return qs.count()

    def check_report_errors(self):
        self.check_finding_errors()
        if not self.report_document.report.recommendation:
            error = ReportError("Missing recommendation!", "#executive-summary-recommendation")
            self._add_error(error)
        if not self.report_document.report.evaluation:
            error = ReportError("Missing evaluation!", "#executive-summary-evaluation")
            self._add_error(error)
        if not self.report_document.report.changehistory_set.count():
            error = ReportError("Change History missing!", "#change-history-table")
            self._add_error(error)


class SingleFindingPDFReport(ErrorMixin, report_types.SingleFindingPDFReport):
    def check_report_errors(self):
        self.check_finding_errors()


class AdvisoryMarkdownExport(report_types.AdvisoryMarkdownExport):
    pass


class AdvisoryPDFExport(report_types.AdvisoryPDFExport):

    def get_context(self):
        context = super().get_context()
        context["now"] = datetime.datetime.now().strftime("%B %d, %Y")
        return context


class VulnerabilityCSVReport(report_types.VulnerabilityCSVReport):
    pass


class PentestExcelReport(report_types.PentestExcelReport):
    pass
