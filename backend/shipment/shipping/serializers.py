from rest_framework import serializers

from products.models import Package, Parcel, Container
from orders.models import Quotation, Order
from shipping.models import Shipping
from location.models import CityCountryServiceProvider, CountryCode


from checkoutdetails.serializers import InvoiceOrderSerializer
from api.v1.serializers.users import AddressSerializer


class ShippringContainersList(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = "__all__"


class ShippingParcelsList(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = "__all__"


class ShippingPackagesList(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"


class CountryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryCode
        fields = "__all__"


class CityCountryServiceProviderSerializer(serializers.ModelSerializer):
    country = CountryCodeSerializer()

    class Meta:
        model = CityCountryServiceProvider
        fields = "__all__"


class ShippingOrderSerializer(serializers.ModelSerializer):
    shipment_origin = AddressSerializer()
    shipment_destination = AddressSerializer()
    origin_city = CityCountryServiceProviderSerializer()
    destination_city = CityCountryServiceProviderSerializer()
    packages = ShippingPackagesList(many=True)
    parcels = ShippingParcelsList(many=True)
    containers = ShippringContainersList(many=True)

    class Meta:
        model = Order
        fields = "__all__"


class ShippingListSerializer(serializers.ModelSerializer):
    order = ShippingOrderSerializer()

    def get_total_cost(self, obj):
        quotation = Quotation.objects.filter(order=obj.order, status=Quotation.STATUS.PAYED).first()
        if quotation:
            return quotation.total_cost
        return None

    class Meta:
        model = Shipping
        fields = "__all__"
