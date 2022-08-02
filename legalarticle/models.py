from django.db import models
from django_extensions.db.models import TimeStampedModel

from laws.models import Law


# Create your models here.

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()


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
    article = models.ForeignKey(LegalArticle, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
