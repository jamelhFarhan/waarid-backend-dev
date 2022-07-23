from django.urls import path

from .views import ContactUs

app_name = "contactus"

urlpatterns = [
    path("contactus/", ContactUs.as_view(), name="contactus"),
]
