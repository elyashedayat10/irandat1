from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager

from categories.models import Category


# Create your models here.
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
    note = models.CharField(max_length=500)

    # def save(self, **kwargs):
    #     self.slug = slugify(self.title)
    #     return super(Law, self).save(**kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('laws:detail', args=[self.id])

    def get_articles_count(self):
        return self.articles.count()
