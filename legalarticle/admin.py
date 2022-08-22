from django.contrib import admin

from .models import ArticleHit, LegalArticle

# Register your models here.

admin.site.register(LegalArticle)
admin.site.register(ArticleHit)
