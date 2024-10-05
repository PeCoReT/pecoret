from attack_surface.models.finding import ProgressStatus
from pecoret.reporting import generators


class AttackSurfaceFindingMixin:
    """
    implements the attack surface finding export method with context
    """
    attack_surface_finding_sections = []

    def get_attack_surface_finding_sections(self):
        return self.attack_surface_finding_sections.copy()

    def export_attack_surface_finding_pdf(self, finding):
        context = self.get_context(**{
            'finding': finding,
            'sections': self.get_attack_surface_finding_sections(),
            'css_body_classes': 'advisory-body',
            'section_head': 'sections/attack_surface/head.html',
        })
        if finding.status == ProgressStatus.DRAFT:
            context['css_body_classes'] = 'advisory-body draft'
        generator = generators.PDFReportGenerator(self, context)
        return generator.generate('pentest_report.html')
