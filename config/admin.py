from django.contrib import admin

from .models import Notification, Setting

# Register your models here.
admin.site.register(Setting)
admin.site.register(Notification)
