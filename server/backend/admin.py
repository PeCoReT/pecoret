from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend import models


class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Customer Info', {'fields': ('company',)}),
    )


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.PentestType)
admin.site.register(models.AssetType)
admin.site.register(models.CustomFieldAsset)
admin.site.register(models.Asset)
