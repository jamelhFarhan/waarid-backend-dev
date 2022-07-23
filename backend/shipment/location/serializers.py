from rest_framework import serializers

from location.models import CityCountryServiceProvider


class CityCountrySerializer(serializers.ModelSerializer):
    search_string = serializers.SerializerMethodField()

    def get_search_string(self, obj):
        return ", ".join([obj.city_name, obj.country.country_name])

    class Meta:
        model = CityCountryServiceProvider
        fields = ["id", "search_string"]
