from pecoret.reporting import generators


class AdvisoryMixin:
    """
    implements the advisory export method with context
    """
    advisory_sections = []

    def get_advisory_sections(self):
        return self.advisory_sections.copy()

    def export_advisory_pdf(self, advisory):
        context = self.get_context(**{
            'advisory': advisory,
            'sections': self.get_advisory_sections(),
            'css_body_classes': 'advisory-body',
            'section_head': 'sections/advisory/head.html',
        })
        generator = generators.PDFReportGenerator(self, context)
        return generator.generate('pentest_report.html')
