# api/v1/views/orders.py

# python
from datetime import date
# Django
from django.db.models import Q

# third party
from rest_framework import viewsets, serializers

# apps
from api.v1.serializers import (
    OrderSerializer, QuotationSerializer, ContactSerializer
)
# from api.v1.permissions import IsModelOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from orders.models import Order, Quotation
from users.models import CustomUser


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsModelOwnerOrAdmin, ]
    http_method_names = ['get', 'put', 'post', 'patch', 'delete', 'head']
    serializer_class = OrderSerializer
    page_size = 20

    def get_queryset(self):
        queryset = []
        user = self.request.user
        if user.is_admin or user.role == CustomUser.ROLE.CARRIER:
            queryset = Order.objects.filter(win_quotation__isnull=True)
        elif user.role == CustomUser.ROLE.CUSTOMER:
            queryset = Order.objects.filter(owner=user)
        if queryset.count() > 0:
            return queryset.order_by('-updated_at')
        return queryset


class QuotationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'post', 'patch', 'delete', 'head']
    serializer_class = QuotationSerializer

    def get_queryset(self):
        queryset = Quotation.objects.all()
        user = self.request.user
        if user.role == CustomUser.ROLE.CARRIER:
            queryset = Quotation.objects.filter(carrier=user)
        # queryset = Quotation.objects.filter(
        #     Q(valid_till_date__isnull=True)
        #     | Q(valid_till_date__gte=date.today())
        # )
        return queryset

    def partial_update(self, request, *args, **kwargs):
        # we don't need this in PATCH
        # there is SEND NOTE button for
        # POST new message on quotation_note
        request.data.pop("notes", None)
        return super().partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        order = Order.objects.get(pk=request.data["order_id"])
        if order.win_quotation:
            raise serializers.ValidationError(
                "The Customer has chosen another Сarrier. Submitting a quote is unavailable"
            )

        return super().create(request, *args, **kwargs)


class ContactViewSet(viewsets.ModelViewSet):
    http_method_names = ['patch']
    serializer_class = ContactSerializer
    queryset = Order.objects.all()
