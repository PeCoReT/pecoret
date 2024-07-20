from django.conf import settings
from pecoret.reporting.template.errors.base import BaseErrorCheck


class FindingProofCheck(BaseErrorCheck):
    message = 'Finding has no proof!'

    def check(self, context, **kwargs):
        errors = []
        findings = context.get('findings', [])
        if context.get('finding'):
            findings = [context['finding']]
        for finding in findings:
            if not finding.proof_text:
                url = self._build_url(
                    settings.SITE_URLS['FINDING_DETAIL'].format(
                        projectId=finding.project.pk, findingId=finding.pk
                    )
                )
                errors.append(
                    self.create_error(
                        'Finding has no proof!', f'#finding-{finding.pk}-proofs', edit_link=url)
                )
        return errors
