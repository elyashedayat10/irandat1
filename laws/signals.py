from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from .models import Law, Chapter
from django.db.models import F


@receiver(pre_delete, sender=Chapter)
def update_chapter_order(sender, **kwargs):
    category_obj = Chapter.objects.get(id=kwargs['instance'].id)
    if category_obj.parent:
        Chapter.objects.filter(parent=category_obj.parent).update(order=F('order') - 1)
    else:
        Chapter.objects.filter(parent=None).update(order=F('order') - 1)


@receiver(pre_delete, sender=Law)
def update_chapter_order(sender, **kwargs):
    category_obj = Law.objects.get(id=kwargs['instance'].id)
    if category_obj.parent:
        Law.objects.filter(parent=category_obj.parent).update(order=F('order') - 1)
    else:
        Law.objects.filter(parent=None).update(order=F('order') - 1)
