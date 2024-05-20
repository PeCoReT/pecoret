from pecoret.reporting.report_plugin import ReportPluginLoader


def export_finding(finding, template):
    plugin_loader = ReportPluginLoader(template)
    plugin = plugin_loader.load_plugin_from_report_template('export_asmonitor_finding')
    result, content_type, extension = plugin.export_asmonitor_finding(finding)
    return result
