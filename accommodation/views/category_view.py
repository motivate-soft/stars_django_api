from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from accommodation.models.category import Category
from accommodation.serializers.category_serializer import CategorySerializer, CategoryItemSerializer


# class CategoryListAPIView(ListAPIView):
#     permission_classes = []
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class CategoryItemsAPIView(ListAPIView):
#     permission_classes = []
#     queryset = Category.objects.all()
#     serializer_class = CategoryItemSerializer
#
#
# class CategoryCreateAPIView(CreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action == 'listing':
            return CategoryItemSerializer
        return CategorySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'listing':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, permission_classes=[], serializer_class=CategoryItemSerializer)
    def listing(self, request):
        category_list = Category.objects.all()
        serializer = self.get_serializer(category_list, many=True)
        return Response(serializer.data)
