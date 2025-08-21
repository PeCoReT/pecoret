from ._base import BASE_DIR


# PECORET general settings
SITE_NAME = 'PeCoReT Project'
SITE_URL = 'http://localhost:8000'


###################
# Report Templates
###################
REPORT_TEMPLATE_PRESETS = {
    'default_template': {
        'path': BASE_DIR / 'resources/report_templates/default_template/report_template.py'
    }
}

REPORT_TEMPLATES = {
    'default_template': {
        'preset': 'default_template',
        'css_files': [BASE_DIR / 'resources/report_templates/default_template/styles/blue.css']
    },
}


############################
# Attack Surface Application
############################

# enable requesting scans in PeCoReT
# the scans are NOT performed by pecoret, just managed. You must add your own tooling
AS_ENABLE_SCANNING = False

# fill the names with scan types that can be triggered on item creation
AS_ALLOWED_SCAN_TYPES_ON_CREATION = []

# ADVISORIES
# Timedelta (in days) for the planned disclosure date of an advisory.
ADVISORY_DISCLOSURE_TIMEDELTA = 60
ADVISORY_ID_PREFIX = 'pecoret-'

AS_REPORT_TEMPLATE = 'default_template'

#########
# Theming
#########
PECO_THEME = 'default'
