from django.contrib import admin
from django import forms

from attack_surface.models.scanner import Scanner
from attack_surface.models.scan_type import ScanType


class ScannerAdminForm(forms.ModelForm):
    class Meta:
        model = Scanner
        fields = ['name', 'scan_types']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ScannerAdmin(admin.ModelAdmin):
    form = ScannerAdminForm
    filter_horizontal = ('scan_types',)

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            self.message_user(request, f'Token for {obj.name}: {obj.token}', level='success')


admin.site.register(Scanner, ScannerAdmin)
admin.site.register(ScanType)
