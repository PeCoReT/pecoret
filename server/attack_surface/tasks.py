from pecoret.reporting.template_loader import ReportTemplateLoader


def export_finding_pdf(finding, template):
    loader = ReportTemplateLoader(template)
    report_template = loader.load()
    result, _, _ = report_template.export_attack_surface_finding_pdf(finding)
    return result


