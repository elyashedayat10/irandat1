from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from .models import Law, Chapter
from django.db.models import F


@receiver(pre_delete, sender=Chapter)
def update_chapter_order(sender, **kwargs):
    category_obj = Chapter.objects.get(id=kwargs['instance'].id)
    if category_obj.parent:
        Chapter.objects.filter(law=category_obj.law, parent=category_obj.parent).filter(
            order__gt=kwargs['instance'].order).update(
            order=F('order') - 1)
    else:
        Chapter.objects.filter(law=category_obj.law, parent=None).filter(order__gt=kwargs['instance'].order).update(
            order=F('order') - 1)


@receiver(pre_delete, sender=Law)
def update_law_order(sender, **kwargs):
    Law.objects.filter(order__gt=kwargs['instance'].order).update(order=F('order') - 1)
