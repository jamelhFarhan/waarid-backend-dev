from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView

from orders.models import Order
from users.models import CustomUser
from .serializers import OrderCheckoutSerializer, OrderPaymentInfoSerializer, InvoicesListSerializer
from checkoutdetails.models import Invoice


class OrderCheckoutViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderCheckoutSerializer


class OrderPaymentInfoViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderPaymentInfoSerializer


class InvoicesListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = InvoicesListSerializer

    def get_queryset(self):  # wait for status query string

        user_role = self.request.user.role
        user = self.request.user

        if user_role == CustomUser.ROLE.CUSTOMER:
            qs = Invoice.objects.filter(quotation__order__owner=user)
        elif user_role == CustomUser.ROLE.CARRIER:
            qs = Invoice.objects.filter(quotation__carrier=user)
        else:
            qs = Invoice.objects.none()

        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=int(status))
        return qs


class InvoiceView(RetrieveAPIView):
    serializer_class = InvoicesListSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "invoice_pk"
    lookup_field = "pk"

    def get_queryset(self):
        return Invoice.objects.filter(quotation__order__owner=self.request.user)
