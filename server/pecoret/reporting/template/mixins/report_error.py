

class ReportErrorMixin:
    """
    mixin to generate report errors

    _error_classes: should have the format of key and class to use
    e.g. {'finding': BasicFindingError}
    """
    _error_classes = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = {}

    def get_error_classes(self):
        return self._error_classes

    def get_errors_for_section(self, section):
        return self.get_errors().get(section, [])

    def get_errors(self):
        """
        return complete errors dict
        """
        return self.errors

    def add_error(self, error):
        """
        add an error to the dict
        """
        if not self.errors.get(error.url):
            self.errors[error.url] = [error]
        else:
            self.errors[error.url].append(error)

    def check_errors(self, identifier, context):
        for error_class in self.get_error_classes().get(identifier):
            instance = error_class()
            errors = instance.check(context)
            if errors:
                for error in errors:
                    self.add_error(error)
