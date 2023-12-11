from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


admin.site.register(models.Project)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.CWE)
admin.site.register(models.VulnerabilityTemplate)
admin.site.register(models.ProjectVulnerability)
admin.site.register(models.Finding)
admin.site.register(models.ReportTemplate)
admin.site.register(models.Company)
admin.site.register(models.Membership)
admin.site.register(models.ReportRelease)
admin.site.register(models.Report)
admin.site.register(models.FindingTimeline)
admin.site.register(models.AuthToken)
admin.site.register(models.CompanyContact)
admin.site.register(models.Advisory)
admin.site.register(models.AdvisoryMembership)
admin.site.register(models.PentestType)
