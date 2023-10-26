from pecoret.core.reporting.error import ReportError
from backend.models import Finding


class ErrorMixin:
    def check_finding_errors(self):
        # check finding errors
        for finding in Finding.objects.for_report(self.get_project()):
            if not finding.proof_text:
                error = ReportError("Missing proof!", f"#finding-{finding.pk}-proofs")
                self._add_error(error)
            if self.get_project().require_cvss_base_score and finding.cvssbasescore.is_incomplete:
                error = ReportError("Missing CVSS base score", f"#finding-{finding.pk}-title")
                self._add_error(error)
