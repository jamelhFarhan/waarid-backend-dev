from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    OrderCheckoutViewSet,
    OrderPaymentInfoViewSet,
    InvoicesListView,
    InvoiceView
)

app_name = "checkoutdetails"

router = DefaultRouter()
router.register(r'order_checkout', OrderCheckoutViewSet)
router.register(r'payment_info', OrderPaymentInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('invoices/', InvoicesListView.as_view()),
    path('invoice/<int:invoice_pk>/', InvoiceView.as_view())
]
