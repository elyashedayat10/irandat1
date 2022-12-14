from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Category


# Register your models here.
@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 40
