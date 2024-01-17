from urllib.parse import urljoin

from django.conf import settings
from extra_settings.models import Setting

from backend.models.project import ScoreChoices
from pecoret.reporting.error import ReportError


class ReportErrorMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = {}

    def build_url(self, path):
        url = Setting.get('GENERAL_SITE_URL')
        return urljoin(url, path)

    def get_errors_for_section(self, section):
        return self.errors.get(section, [])

    def get_errors(self):
        return self.errors

    def add_error(self, error):
        if not self.errors.get(error.url):
            self.errors[error.url] = [error]
        else:
            self.errors[error.url].append(error)

    def _check_finding_errors(self, context):
        findings = context.get('findings', [])
        if context.get('finding'):
            findings = [context['finding']]
        for finding in findings:
            if not finding.proof_text:
                url = self.build_url(
                    settings.SITE_URLS['FINDING_DETAIL'].format(
                        projectId=finding.project.pk, findingId=finding.pk)
                )
                error = ReportError("Missing proof!", f"#finding-{finding.pk}-proofs", edit_link=url)
                self.add_error(error)
            if context.get('project') and context['project'].require_cvss_score is not None:
                score = ScoreChoices(context['project'].require_cvss_score)
                if score == ScoreChoices['CVSS31_BASE']:
                    if not finding.cvss_score_31:
                        url = self.build_url(settings.SITE_URLS['FINDING_SCORES'].format(projectId=finding.project.pk,
                                                                                         findingId=finding.pk))
                        error = ReportError(
                            "Missing CVSS base score", f"#finding-{finding.pk}-title", edit_link=url)
                        self.add_error(error)
                elif score == ScoreChoices['CVSS4_BASE']:
                    if not finding.cvss_score_40:
                        url = self.build_url(settings.SITE_URLS['FINDING_SCORES'].format(projectId=finding.project.pk,
                                                                                         findingId=finding.pk))
                        error = ReportError(
                            "Missing CVSS base score", f"#finding-{finding.pk}-title", edit_link=url)
                        self.add_error(error)

    def check_pdf_report_errors(self, context):
        self._check_finding_errors(context)
        if context.get('report_document'):
            report = context['report_document'].report
            if not report.recommendation:
                error = ReportError("Missing recommendation!", "#executive-summary-recommendation")
                self.add_error(error)
            if not report.evaluation:
                error = ReportError("Missing evaluation!", "#executive-summary-evaluation")
                self.add_error(error)
            if not report.changehistory_set.count():
                error = ReportError("Change History missing!", "#change-history-table")
                self.add_error(error)
