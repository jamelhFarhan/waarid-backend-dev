from django.urls import path
from location.views import CityCountry


app_name = "location"
urlpatterns = [
    path("city-country/", CityCountry.as_view()),
]
