# api/v1/views/users.py

from rest_framework import viewsets

from api.v1.serializers import CustomUserSerializer, CompanySerializer
from api.v1.permissions import IsOwnerOrAdmin, IsModelOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser, Company


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete', 'head']
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        queryset = []
        if self.request.user.is_admin:
            queryset = CustomUser.objects.all()
        else:
            queryset = CustomUser.objects.filter(id=self.request.user.id)
        return queryset


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsModelOwnerOrAdmin, IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete', 'head']
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = []
        if self.request.user.is_admin:
            queryset = Company.objects.all()
        else:
            queryset = Company.objects.filter(owner=self.request.user)
        return queryset
