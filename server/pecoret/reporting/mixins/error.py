from ..error import ReportError


class ErrorMixin:
    """
    checks if the rendered report contains any errors. (e.g. a finding is missing a proof)
    """
    report_errors = {}

    def get_report_errors(self):
        return self.report_errors.copy()

    def add_report_error(self, message, url):
        error = ReportError(message, url)
        if not self.report_errors.get(error.url):
            self.report_errors[error.url] = [error]
            return
        self.report_errors[error.url].append(error)

    def get_report_errors_for_section(self, section):
        return self.report_errors.get(section, [])

    def check_report_errors(self):
        pass
