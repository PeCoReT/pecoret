from pecoret.settings import *

# -------------------------------------------------
# Basic Project Settings
# -------------------------------------------------
# Define a list of allowed hosts (domains or IPs) to access the application.
# ALLOWED_HOSTS = ["127.0.0.1", "localhost", "example.com"]

# DEBUG: Controls debug mode. When True, Django provides detailed error pages.
# Disable this in production as it can reveal sensitive information.
# DEBUG = True

# ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
# CORS_ALLOWED_ORIGINS = ["https://pecoret.example.com"]
# CSRF_TRUSTED_ORIGINS = []

# -------------------------------------------------
# Session and Site Settings
# -------------------------------------------------

# SESSION_COOKIE_AGE: Expire user session after a specified time (in seconds).
# Example sets it to 15 minutes, commonly used to ensure inactive sessions end.
# SESSION_COOKIE_AGE = 15 * 60

# SITE_NAME: used in various settings and templates mostly in emails.
# SITE_URL: URL of the site, used to generate links, especially for emails.
# SITE_NAME = "pecoret.example.com"
# SITE_URL = 'http://localhost:8000

# SECURE_PROXY_SSL_HEADER: Required when using a reverse proxy for SSL termination.
# This tells Django to trust a specified header to detect HTTPS requests.
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -------------------------------------------------
# Security Settings
# -------------------------------------------------
# CORS_ALLOWED_ORIGINS: Specify trusted origins allowed to make CORS requests.
# This is necessary if your app's frontend and backend are hosted separately.
# CORS_ALLOWED_ORIGINS = ["https://example-frontend.com"]

# CSRF_TRUSTED_ORIGINS: Define origins trusted for Cross-Site Request Forgery (CSRF) protection.
# This is particularly important for cross-domain requests to prevent CSRF attacks.
# CSRF_TRUSTED_ORIGINS = ["https://example-frontend.com"]

# CSRF_COOKIE_SAMESITE: Controls the 'SameSite' attribute for the CSRF cookie, which helps prevent
# cross-site request forgery (CSRF) attacks. "Strict" enforces that the CSRF cookie is only sent
# with requests originating from the same site, enhancing security.
# CSRF_COOKIE_SAMESITE = "Strict"

# SESSION_COOKIE_SAMESITE: Controls the 'SameSite' attribute for session cookies.
# Setting this to "Strict" means that the session cookie will only be sent with requests
# initiated from the same site. This reduces the risk of session hijacking from external sites.
# SESSION_COOKIE_SAMESITE = "Strict"

# CSRF_COOKIE_SECURE: Ensures the CSRF cookie is only sent over HTTPS connections.
# For production, set this to True to protect against man-in-the-middle (MITM) attacks.
# Only use False in development environments that lack HTTPS.
# CSRF_COOKIE_SECURE = True

# SESSION_COOKIE_SECURE: Ensures the session cookie is only sent over HTTPS.
# Set this to True in production environments with HTTPS enabled for security.
# SESSION_COOKIE_SECURE = True

# -------------------------------------------------
# Database Configuration
# -------------------------------------------------

# DATABASES: Configure database connections for the application.
# This example is configured for PostgreSQL, but other backends (e.g., MySQL, SQLite)
# can be used by adjusting the ENGINE setting.
#    DATABASES = {
#        'default': {
#            'ENGINE': 'django.db.backends.postgresql',
#            'HOST': 'localhost',
#            'NAME': 'pecoret',
#            'USER': 'pecoret',
#            'PASSWORD': 'secure'
#        },
#    }

# -------------------------------------------------
# Report Templates Settings
# -------------------------------------------------

# REPORT_TEMPLATES: Define custom templates for reports.
# REPORT_TEMPLATES = {
#    'default_template': {
#        'preset': 'default_template',
#        'css_files': [BASE_DIR / 'resources/report_templates/default_template/styles/blue.css']
#    },
#    'lime': {
#        'preset': 'default_template',
#        'css_files': [BASE_DIR / 'resources/report_templates/default_template/styles/lime.css'],
#    },
# }

# -------------------------------------------------
# Logging Configuration
# -------------------------------------------------

# LOGGING: Configure logging to monitor and record various events. This example uses
# a file handler to store logs in a specified file. The logging level is set to DEBUG
# for development. Adjust log level or add more handlers based on environment needs.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/opt/pecoret/debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

# -------------------------------------------------
# Email Settings
# -------------------------------------------------
# EMAIL_BACKEND: The backend used to send emails. SMTP is the standard for production.
# EMAIL_USE_SSL: Enables SSL for secure email transmission.
# EMAIL_HOST: SMTP server used to send emails.
# EMAIL_PORT: Port for SMTP over SSL, usually 465 for secure connections.
# EMAIL_HOST_USER: SMTP server username, often the sender email.
# EMAIL_HOST_PASSWORD: SMTP server password.
# DEFAULT_FROM_EMAIL: Default email address for sending out messages.
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_SSL = True
# EMAIL_HOST = "mail.example.com"
# EMAIL_PORT = 465
# EMAIL_HOST_USER = "noreply@example.com"
# EMAIL_HOST_PASSWORD = "mysecurepassword"
# DEFAULT_FROM_EMAIL = "noreply@example.com"

# -------------------------------------------------
# Advisory Application Settings
# -------------------------------------------------

# ADVISORY_ID_PREFIX: Prefix used for advisory identifiers. (e.g. ADV-2024-0001)
# ADVISORY_ID_PREFIX = "ADV-"

# -------------------------------------------------
# Attack Surface Monitoring Settings
# -------------------------------------------------

# AS_ENABLE_SCANNING: Toggle scanning capabilities in the attack surface application.
# AS_ENABLE_SCANNING = False

# AS_REPORT_TEMPLATE: key of the report template to use for Attack Surface related Findings
# AS_REPORT_TEMPLATE = 'default'

# ----------------------------------------
# Theming
# ----------------------------------------
# determined using the filename in the `frontend/presets/` directory
# PECO_THEME = 'aura'
# initial background color to bypass white pages on page reloads with PrimeVue4
# PECO_THEME_INIT_BG_COLOR = '#020617'
