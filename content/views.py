from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from content.models import Content
from content.serializer import ContentSerializer


class ContentListView(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentCreate(CreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
