from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

user = settings.AUTH_USER_MODEL


# Create your models here.


class Comment(TimeStampedModel):
    legal_article = models.ForeignKey(
        "legalarticle.LegalArticle", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="user_comments"
    )
    content = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )

    def __str__(self):
        return f"{self.user} commrnt on {self.legal_article}"
