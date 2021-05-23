from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_meta.models import ModelMeta
from django_meta.serializer import MetaSerializer


class MetaViewSet(viewsets.ModelViewSet):
    queryset = ModelMeta.objects.all()
    serializer_class = MetaSerializer

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        return serializer_class

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # custom retrieve function for both slug and id
    def retrieve(self, request, *args, **kwargs):
        if kwargs['pk'].isdigit():
            return super().retrieve(request, *args, **kwargs)
        else:
            queryset = self.filter_queryset(self.get_queryset())

            filter_kwargs = {'slug': self.kwargs['pk']}
            obj = get_object_or_404(queryset, **filter_kwargs)

            self.check_object_permissions(self.request, obj)
            serializer = self.get_serializer(obj)
            return Response(serializer.data)
