from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


class Category(MPTTModel):
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="دسته مادر",
    )
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="عنوان",
    )
    order = models.PositiveIntegerField(null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["order"]

    def __str__(self):
        return self.title
