from django.db.models.signals import post_delete
from django.db.models import F
from django.dispatch import receiver
from .models import Category


@receiver(post_delete, sender=Category)
def update_category_order(sender, **kwargs):
    Category.objects.filter(order__gt=kwargs['instance'].order).update(order=F('order') - 1)
