from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager

from categories.models import Category


class Law(TimeStampedModel):
    title = models.CharField(max_length=500)
    tags = TaggableManager()
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.CASCADE,
        related_name="laws",
        null=True,
        blank=True,
    )
    approved = models.DateField()
    published = models.DateField()
    approval_authority = models.CharField(max_length=125)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("laws:detail", args=[self.id])

    def get_articles_count(self):
        return self.articles.count()

    def chapters_count(self):
        return self.chapters.count()


class Chapter(models.Model):
    number = models.CharField(max_length=125)
    law = models.ForeignKey(Law, on_delete=models.CASCADE, related_name="chapters")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="child", null=True, blank=True)

    def __str__(self):
        return f"{self.number} from {self.law}"

    def article_count(self):
        return self.articles.all()
