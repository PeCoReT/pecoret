from django.core.validators import RegexValidator


generic_url_validator = RegexValidator(
    regex=(
        r"^[a-zA-Z][a-zA-Z0-9+.-]*://"  # scheme
        r"(([a-zA-Z0-9.-]+)|"  # domain
        r"(\d{1,3}(\.\d{1,3}){3}))"  # or IPv4
        r"(:\d+)?"  # optional port
        r"(/[^\s]*)?$"  # optional path
    ),
    message="Enter a valid URL with a valid scheme (e.g. scheme://host[:port][/path]).",
    code="invalid_generic_url",
)
