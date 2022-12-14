from django.urls import reverse
from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager

from laws.models import Chapter, Law
from django.contrib.contenttypes.fields import GenericRelation

from comment.models import Comment

user = settings.AUTH_USER_MODEL


# Create your models here.


class LegalArticle(TimeStampedModel):
    _type = models.TextField(blank=True)
    _type2 = models.TextField(blank=True)
    description = models.TextField()
    approved = models.DateField()
    tags = TaggableManager()
    law = models.ForeignKey(
        "laws.Law", on_delete=models.CASCADE, related_name="articles"
    )
    number = models.PositiveIntegerField(blank=True, null=True)
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="articles",
        blank=True,
        null=True,
    )
    comments = GenericRelation(Comment)

    class Meta:
        permissions = (
            ("ایجاد ماده", "دسترسی به ایجاد ماده"),
            ("به روزرسانی ماده", "دسترسی به بروزرسانی ماده"),
            ("حذف  ماده", "دسترسی به حذف ماده"),
        )

    def __str__(self):
        return f"ماده شماره {self.number} از قانون {self.law}"

    def get_absolute_url(self):
        return reverse("legal:detail", kwargs={"id": self.id})

    @property
    def get_hist_count(self):
        return self.hits.all().count()


class ArticleHit(models.Model):
    article = models.ForeignKey(
        LegalArticle, on_delete=models.CASCADE, related_name="hits"
    )
    operating_system = models.CharField(max_length=125, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    previous_page = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=125)


class Favorite(models.Model):
    article = models.ForeignKey(
        LegalArticle, on_delete=models.CASCADE, related_name="favorites"
    )
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="likes")


class Dislike(models.Model):
    article = models.ForeignKey(
        LegalArticle, on_delete=models.CASCADE, related_name="dislike"
    )
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="dislikes")
