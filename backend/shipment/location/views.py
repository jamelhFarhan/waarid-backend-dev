from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from location.models import CityCountryServiceProvider


from location.serializers import CityCountrySerializer
from location.paginators import CityCountryPagination


class CityCountry(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CityCountrySerializer
    pagination_class = CityCountryPagination

    def get_queryset(self):
        search_string = self.request.query_params.get(
            "search"
        )  # it waits for the "search" query parameter
        chosen_city_id = self.request.query_params.get("city_id")
        results = {}
        if chosen_city_id is not None:
            chosen_country = CityCountryServiceProvider.objects.get(
                id=chosen_city_id
            ).country.country_code
            if chosen_country == "SA":
                results = CityCountryServiceProvider.objects.exclude(
                    country__country_code="SA"
                ).order_by("country__country_name")
            else:
                results = CityCountryServiceProvider.objects.filter(
                    country__country_code="SA"
                )
        else:
            results = CityCountryServiceProvider.objects.order_by(
                "-country__priority", "country__country_name"
            )

        if search_string is not None:
            results = results.filter(
                Q(city_name__istartswith=search_string)
                | Q(country__country_name__icontains=search_string),
                country__active=True,
            )

        return results
