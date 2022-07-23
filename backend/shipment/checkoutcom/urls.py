from django.urls import path

from .views import CheckoutcomPay

urlpatterns = [
    path("checkoutcom_pay/<int:quotation_id>", CheckoutcomPay.as_view()),
]
