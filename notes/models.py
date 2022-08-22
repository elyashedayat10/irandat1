from django.db import models

from legalarticle.models import LegalArticle

# Create your models here.


class Note(models.Model):
    article = models.ForeignKey(
        LegalArticle, on_delete=models.CASCADE, related_name="notes"
    )
    description = models.TextField()
