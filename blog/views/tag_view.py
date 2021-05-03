from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

from blog.models import Tag
from blog.serializers.tag_serializer import TagSerializer, TagItemSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_serializer_class(self):
        if self.action == 'listing':
            return TagItemSerializer
        return TagSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'listing':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, permission_classes=[], serializer_class=TagItemSerializer)
    def listing(self, request):
        tag_list = Tag.objects.all()
        serializer = self.get_serializer(tag_list, many=True)
        return Response(serializer.data)
