from django.contrib import admin
from .models.webhook import Webhook


admin.site.register(Webhook)
