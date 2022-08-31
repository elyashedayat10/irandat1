from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Law, Chapter
from django.db.models import F


@receiver(post_delete, sender=Law)
def update_law_order(sender, **kwargs):
    Law.objects.filter(order__gt=kwargs['instance'].order).update(F('order') - 1)


@receiver(post_delete, sender=Chapter)
def update_chapter_order(sender, **kwargs):
    Chapter.objects.filter(order__gt=kwargs['instance'].order).update(F('order') - 1)
