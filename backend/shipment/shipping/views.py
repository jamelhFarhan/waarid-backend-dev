import logging

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from shipping.models import Shipping
from shipping.serializers import ShippingListSerializer
from orders.models import Order, Quotation
from products.models import Package


logger = logging.getLogger(__name__)


class ShippingList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShippingListSerializer

    def get_queryset(self):
        if self.request.user.role == 1:  # user is customer
            qs = Shipping.objects.filter(order__owner=self.request.user)
        elif self.request.user.role == 3:  # user is carrier
            qs = Shipping.objects.filter(order__pk__in=Quotation.objects.filter(carrier=self.request.user)
                                         .values_list("order__pk", flat=True))
        else:
            return Shipping.objects.none()

        if self.request.query_params.get("status"):
            try:
                status = int(self.request.query_params.get("status"))
            except ValueError:
                return Shipping.objects.none()
            qs = qs.filter(status=status)

        return qs
