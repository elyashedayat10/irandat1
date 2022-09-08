from django.db.models import F
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from ..models import Category
from .serializers import CategorySerializer


class CategoryListApiView(ListAPIView):
    queryset = Category.objects.filter(parent=None).order_by("order")
    serializer_class = CategorySerializer
    permission_classes = [
        AllowAny,
    ]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"message": "category list", "data": response.data})


class CategoryCreateAPIView(CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [
        IsAdminUser,
    ]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "item created", "data": response.data})

    def perform_create(self, serializer):
        obj = serializer.save()
        if obj.parent:
            Category.objects.filter(parent=obj.parent, order__gte=obj.order).exclude(id=obj.id).update(
                order=F('order') + 1)
        else:
            Category.objects.filter(parent=None, order__gte=obj.order).exclude(id=obj.id).update(
                order=F('order') + 1)


class CategoryUpdateApiView(UpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [
        IsAdminUser,
    ]

    def perform_update(self, serializer):
        order_number = serializer.validated_data['order']
        current_number = Category.objects.get(id=self.get_object().id)
        if order_number > current_number.order:
            if current_number.parent:
                Category.objects.filter(parent=current_number.parent,
                                       order__range=(order_number - 1, current_number.order + 2)).update(
                    order=F('order') - 1)
                # correct
                # Chapter.objects.filter(parent=current_number.parent, order__gte=order_number).exclude(
                #     id=current_number.id).update(
                #     order=F('order') + 1)
                # Chapter.objects.filter(parent=current_number.parent).filter(order__lt=order_number,
                #                                                             order__gte=current_number.order).exclude(
                #     id=current_number.id).update(
                #     order=F('order') - 1)
                print("reza")
            else:
                Category.objects.filter(parent=None,
                                       order__range=(order_number - 1, current_number.order + 2)).update(
                    order=F('order') - 1)
                # Chapter.objects.filter(parent=None, order__gt=order_number).exclude(id=current_number.id).update(
                #     order=F('order') + 1)
                # Chapter.objects.filter(parent=None).filter(
                #     Q(order__lt=order_number) | Q(order__gt=current_number.order)).exclude(
                #     id=current_number.id).update(
                #     order=F('order') - 1)
                # correct
                print("abbas")
        elif order_number == current_number.order:
            pass
        else:
            if current_number.parent:
                Category.objects.filter(parent=current_number.parent,
                                       order__range=(order_number, current_number.order - 1)).update(
                    order=F('order') + 1)
                # Chapter.objects.filter(parent=current_number.parent, order__lte=order_number,
                #                        order__gt=current_number.order).exclude(
                #     id=current_number.id
                # ).update(order=F('order') - 1)
                print("ilghar")
            else:
                #
                # Chapter.objects.filter(parent=None, order__gte=order_number).exclude(
                #     id=current_number.id, order__lt=current_number.order
                # ).update(order=F('order') + 1)
                Category.objects.filter(parent=None,
                                       order__range=(order_number, current_number.order - 1)).update(
                    order=F('order') + 1)

                # Chapter.objects.filter(parent=None, order__lte=order_number, order__gt=current_number.order).exclude(
                #     id=current_number.id
                # ).update(order=F('order') - 1)
                print("elyas")
        serializer.save()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "item updated", "data": response.data})


class CategoryDeleteApiView(DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [
        IsAdminUser,
    ]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response(
            {
                "message": "item deleted",
            }
        )

#
# class CategoryLawApiView(ListAPIView):
#     # queryset=
#     serializer_class=
#     # def get_queryset(self):
#         # queryset = super(ProfessorReviewList, self).get_queryset()
#         # return queryset.filter(professor__pk=self.kwargs.get('pk'))
#
#     def get_queryset(self):
#         return Law.objects.filter(category_id=self.kwargs.get('id'))
