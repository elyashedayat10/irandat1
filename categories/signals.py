from django.db.models.signals import pre_delete
from django.db.models import F
from django.dispatch import receiver
from .models import Category


@receiver(pre_delete, sender=Category)
def update_category_order(sender, **kwargs):
    category_obj = Category.objects.get(id=kwargs['instance'].id)
    print(
        "eluas"
    )
    if category_obj.parent:
        test = Category.objects.filter(parent=category_obj.parent).filter(order__gt=kwargs['instance'].order).update(
            order=F('order') - 1)
        print("ilghar")
        print(test)
    else:
        test = Category.objects.filter(parent=None).filter(order__gt=kwargs['instance'].order).update(
            order=F('order') - 1)
        print("reza")
        print(test)
