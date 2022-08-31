from django.db.models.signals import post_save
from django.db.models import F
from django.dispatch import receiver
from .models import Category


@receiver(post_save, sender=Category)
def update_order(sender, **kwargs):
    if kwargs['created']:
        updated_category = Category.objects.get(order=kwargs['instance'].order)
        Category.objects.filter(order__gt=updated_category.order).update(F('order') + 1)
