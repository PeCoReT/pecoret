from django import forms
from django.contrib import admin

from attack_surface.models.scanner import Scanner
from . import models


class ScannerAdminForm(forms.ModelForm):
    class Meta:
        model = Scanner
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ScannerAdmin(admin.ModelAdmin):
    form = ScannerAdminForm

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            self.message_user(
                request, f"Token for {obj.name}: {obj.token}", level="success"
            )


class TargetAdmin(admin.ModelAdmin):
    search_fields = ("data",)


class ServiceAdmin(admin.ModelAdmin):
    search_fields = ("service_name",)


class URLAdmin(admin.ModelAdmin):
    search_fields = ("url",)


admin.site.register(Scanner, ScannerAdmin)
admin.site.register(models.Target, TargetAdmin)
admin.site.register(models.URL, URLAdmin)
admin.site.register(models.Service, ServiceAdmin)
