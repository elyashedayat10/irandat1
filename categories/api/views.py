from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Category
from .serializers import CategorySerializer


class CategoryListApiView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'message': 'category list',
            'data': response.data
        })


class CategoryCreateAPIView(CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'item created',
            'data': response.data
        })


class CategoryUpdateApiView(UpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'item updated',
            'data': response.data
        })


class CategoryDeleteApiView(DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            'message': 'item deleted',
        })

    # def get_queryset(self):
    #     queryset = super(CategoryListApiView, self).get_queryset()
    #     return queryset.filter(professor__pk=self.kwargs.get('pk'))

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


# class ProfessorReviewList(generics.ListCreateAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get_queryset(self):
#         queryset = super(ProfessorReviewList, self).get_queryset()
#         return queryset.filter(professor__pk=self.kwargs.get('pk'))
#
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsAuthorOrReadOnly,)
#
#     def perform_create(self, serializer):
#         # The request user is set as author automatically.
#         serializer.save(author=self.request.user)
