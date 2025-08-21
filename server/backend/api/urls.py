from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import viewsets

app_name = "backend"

router = DefaultRouter()
router.register('projects', viewsets.ProjectViewSet)
router.register(
    "vulnerability-templates",
    viewsets.VulnerabilityTemplateViewSet,
    "vulnerability-template",
)

router.register(
    'asset-types',
    viewsets.AssetTypeViewSet,
    'asset-type'
)

router.register("companies", viewsets.CompanyViewSet, "company")
router.register("cwes", viewsets.CWEViewSet, "cwe")
router.register('technologies', viewsets.TechnologyViewSet, 'technology')
router.register('custom-fields-asset', viewsets.CustomFieldAssetViewSet, 'custom-field-asset')
router.register("users", viewsets.UserViewSet, "user")
router.register("groups", viewsets.GroupViewSet, "group")

router.register("pentest-types", viewsets.PentestTypeViewSet, "pentest-type")
router.register("api-tokens", viewsets.APITokenViewSet, "api-token")

# company routes
company_router = DefaultRouter()
company_router.register("contacts", viewsets.CompanyContactViewSet, "contact")
company_router.register("information", viewsets.CompanyInformationViewSet, "information")

# project routes
project_router = DefaultRouter()
project_router.register(
    "vulnerabilities", viewsets.ProjectVulnerabilityViewSet, "vulnerability"
)

project_router.register('assets', viewsets.AssetViewSet, 'asset')

project_router.register("findings", viewsets.FindingViewSet, "finding")
project_router.register("accounts", viewsets.AccountViewSet, "account")
project_router.register("reports", viewsets.ProjectReportViewSet, "report")
project_router.register("memberships", viewsets.MembershipViewSet, "membership")
project_router.register(
    "contacts", viewsets.ProjectContactViewSet, "contact"
)
project_router.register("files", viewsets.ProjectFileViewSet, "file")
project_router.register("commands", viewsets.ProjectCommandViewSet, "command")
project_router.register("scopes", viewsets.ProjectScopeViewSet, "scope")
project_router.register('notes', viewsets.ProjectNoteViewSet, 'note')

# finding routes
finding_router = DefaultRouter()
finding_router.register("timelines", viewsets.FindingTimelineViewSet, "timeline")
finding_router.register("comments", viewsets.FindingCommentViewSet, "comment")
finding_router.register("attachments", viewsets.FindingImageAttachmentViewSet, "attachment")

# reports routes
report_router = DefaultRouter()
report_router.register(
    "report-releases", viewsets.ReportReleaseViewSet, "report-release"
)
report_router.register(
    "change-histories", viewsets.ChangeHistoryViewSet, "change-history"
)

urlpatterns = [
    path("", include(router.urls)),
    path("cvss-calculator/4.0/", views.CVSS4CalculatorView.as_view(), name='cvss4-calculator'),
    path("cvss-calculator/3.1/", views.CVSS31CalculatorView.as_view(), name='cvss31-calculator'),
    path("render-markdown/", views.RenderMarkdownToHTML.as_view(), name='render-markdown'),
    path('report-templates/', views.ReportTemplateView.as_view(), name='report-templates'),
    path("projects/<int:project>/", include(project_router.urls)),
    path(
        "projects/<int:project>/findings/<int:finding>/",
        include((finding_router.urls, "backend"), namespace="findings"),
    ),
    path("projects/<int:project>/reports/<int:report>/", include(report_router.urls)),

    path(
        "companies/<int:company>/",
        include((company_router.urls, "backend"), namespace="companies"),
    ),
]
