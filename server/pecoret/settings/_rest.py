from ._base import DEBUG

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "pecoret.core.authentication.APITokenAuthentication"
    ],
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S",
    "DEFAULT_PAGINATION_CLASS": "pecoret.core.pagination.PeCoReTPageNumberPagination",
    "PAGE_SIZE": 100,
    "PAGE_SIZE_QUERY_PARAM": "limit",
    "MAX_PAGINATE_BY": 500,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_RATES": {"auth_flow_throttle": "7/hour"},
    "EXCEPTION_HANDLER": "pecoret.core.exceptions.handle",
    #"DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "PeCoReT API",
    "DESCRIPTION": "PeCoReT API documentation",
    "VERSION": '0.3.0',
    "SERVE_INCLUDE_SCHEMA": False,
    "ENUM_GENERATE_CHOICE_DESCRIPTION": False,
    "COMPONENT_SPLIT_REQUEST": True,
    'EXTENSIONS_ROOT': {
        'x-tagGroups': [
            {
                'name': 'General',
                'tags': ['Authentication', 'API Tokens']
            },
            {
                'name': 'Projects',
                'tags': ['Projects', 'Reporting', 'Accounts', 'Findings', 'Vulnerabilities', 'Project Checklists']
            },
            {
                'name': 'Advisories',
                'tags': ['Advisories', 'Advisory Statistics']
            },
            {
                'name': 'Attack Surface',
                'tags': ['Attack Surface', 'Attack Surface Scanning']
            },
            {
                'name': 'Knowledge Base',
                'tags': [
                    'Knowledge Base', 'Vulnerability Templates', 'Report Templates', 'Technologies',
                    'CWEs', 'Checklists'
                ]
            },
            {
                'name': 'Administration',
                'tags': ['Administration', 'Settings', 'Groups', 'Pentest Types']
            },
            {
                'name': 'Miscellaneous',
                'tags': [
                    'Miscellaneous', 'checks', 'Helpers', 'CVSS Calculator', 'Companies', 'Users'
                ]
            }
        ]
    },
    "ENUM_NAME_OVERRIDES": {
        "FindingStatus": "backend.models.finding.FindingStatus.choices",
        "AssetTaskStatus": "checklists.models.item.ItemStatus.choices",
        "MembershipRoles": "backend.models.membership.Roles.choices",
        "AdvisoryRoles": 'advisories.models.advisory_membership.Roles',
        "AdvisoryVisibilityChoices": 'advisories.models.advisory.VisibilityChoices.choices',
        "ProjectVisibilityChoices": 'backend.models.project.Visibility.choices',

    },
}

CORS_EXPOSE_HEADERS = ["Content-Disposition", "Content-Type"]
CORS_ALLOW_CREDENTIALS = True


SITE_URLS = {
    "PASSWORD_RESET": "/#/reset-password/{uid}/{token}",
    "ACTIVATION": "/#/account-activation/{uid}/{token}",
    "ADVISORY_DETAIL": "/#/advisories/{advisoryId}",
    "FINDING_DETAIL": "/#/projects/{projectId}/findings/{findingId}",
    "CHANGE_EMAIL": "/#/user/change-email/{uid}/{token}",
    'FINDING_SCORES': '/#/projects/{projectId}/findings/{findingId}/scores',
    "ADVISORY_SHARE_TOKEN_DOWNLOAD": '/#/advisories/{advisoryId}/download/{token}'
}



### Django Vite
DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        'dev_server_port': '3000',
        'static_url_prefix': 'dist'
    }
}
