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


class CategoryUpdateApiView(UpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [
        IsAdminUser,
    ]

    def perform_update(self, serializer):
        order_number = serializer.validated_data['order']
        current_number = self.get_object().order
        if order_number > current_number:
            print("ali")
            if self.get_object().parent:
                category_obj = Category.objects.filter(parent=self.get_object().parent)
                category_obj.filter(order__gte=order_number).update(order=F('order') + 1)
            else:
                category_obj = Category.objects.filter(parent=None)
                print(category_obj)
                category_obj.filter(order__gte=order_number).update(order=F('order') + 1)
        elif order_number == current_number:
            pass
        else:
            print("reza")
            if self.get_object().parent:
                category_obj = Category.objects.filter(parent=self.get_object().parent)
                category_obj.filter(order__lte=order_number).update(order=F('order') - 1)
                print("elyas")
            else:
                print("ilghar")
                category_obj = Category.objects.filter(parent=None)
                category_obj.filter(order__lte=order_number).update(order=F('order') + 1)
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
