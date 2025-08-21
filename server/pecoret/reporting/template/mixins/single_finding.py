from pecoret.reporting import generators


class SingleFindingMixin:
    """
    implements the single finding export method with finding related context
    """

    def get_single_finding_context(self, finding):
        sections = [
            'single_finding.html'
        ]
        context = self.get_context(**{
            'section_head': 'head.html',
            'finding': finding,
            'project': finding.project,
            'sections': sections
        })
        return context

    def export_single_finding(self, finding):
        context = self.get_single_finding_context(finding)
        generator = generators.PDFReportGenerator(self, context, language=finding.project.language)
        return generator.generate('pentest_report.html')
