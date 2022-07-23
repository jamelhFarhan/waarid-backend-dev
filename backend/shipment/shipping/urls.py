from django.urls import path

from shipping.views import ShippingList

app_name = "shipping"

urlpatterns = [
    path("shippings-list/", ShippingList.as_view())  # wait for status query parameter, status - int
]
