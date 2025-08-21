from django.contrib import admin

from attack_surface.scanning.models import ExclusionRule, ScanRule, ScanBatchRequest
from attack_surface.scanning.models.scan_template import ScanTemplate


class ExclusionRuleAdmin(admin.ModelAdmin):
    autocomplete_fields = ("target", "service", "url")


# Register your models here.
admin.site.register(ScanTemplate)
admin.site.register(ExclusionRule, ExclusionRuleAdmin)
admin.site.register(ScanRule)
admin.site.register(ScanBatchRequest)
