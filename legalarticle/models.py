from django.db import models
from django_extensions.db.models import TimeStampedModel

from laws.models import Law


# Create your models here.


class LegalArticle(TimeStampedModel):
    description = models.TextField()
    approved = models.DateField()
    law = models.ForeignKey(
        "laws.Law", on_delete=models.CASCADE, related_name="articles"
    )
    number = models.PositiveIntegerField()
    note = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'ماده شماره {self.number} از قانون {self.law}'


class ArticleHit(models.Model):
    article = models.ForeignKey(LegalArticle, on_delete=models.CASCADE,related_name="hits")
    operating_system = models.CharField(max_length=125, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    previous_page = models.URLField(null=True,blank=True)
    location = models.CharField(max_length=125)
