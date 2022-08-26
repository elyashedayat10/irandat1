from django.contrib import admin

from .models import Setting, Notification

# Register your models here.
admin.site.register(Setting)
admin.site.register(Notification)
