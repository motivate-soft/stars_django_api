from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from company.models import Company
from company.serializer import CompanyListingSerializer, CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_serializer_class(self):
        if self.action == 'listing' or self.action == 'list':
            return CompanyListingSerializer
        return CompanySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'listing':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def listing(self, request):
        queryset = Company.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
