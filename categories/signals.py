from django.db.models.signals import pre_delete
from django.db.models import F
from django.dispatch import receiver
from .models import Category


@receiver(pre_delete, sender=Category)
def update_category_order(sender, **kwargs):
    category_obj = Category.objects.get(id=kwargs['instance'].id)
    if category_obj.parent:
        Category.objects.filter(parent=category_obj.parent).update(order=F('order') - 1)
    else:
        Category.objects.filter(parent=None).update(order=F('order') - 1)
