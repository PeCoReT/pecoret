from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from backend import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.PentestType)
admin.site.register(models.AssetType)
