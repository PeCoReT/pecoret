from pecoret.reporting.template import TemplateLoader


def export_single_finding(finding, template):
    loader = TemplateLoader(template)
    RenderableReport = loader.load_template_class("SingleFindingPDFReport")
    result = RenderableReport(loader.template, finding=finding).generate()
    return result


def export_advisory(advisory, template):
    # pylint: disable=invalid-name
    loader = TemplateLoader(template)
    RenderableReport = loader.load_template_class("AdvisoryPDFExport")
    result = RenderableReport(
        loader.template, advisory=advisory
    ).generate()
    return result


def export_advisory_markdown(advisory, template):
    # pylint: disable=invalid-name
    loader = TemplateLoader(template)
    RenderableReport = loader.load_template_class("AdvisoryMarkdownExport")
    result = RenderableReport(
        loader.template, advisory=advisory
    ).generate()
    return result
