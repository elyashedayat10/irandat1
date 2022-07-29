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

    def __str__(self):
        return f'ماده شماره {self.number} از قانون {self.law}'
