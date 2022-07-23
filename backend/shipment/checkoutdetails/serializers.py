from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from django.db import transaction

from api.v1.serializers.users import AddressSerializer
from .models import DeyaratContactCompany, DeyaratContact, Invoice
from orders.models import Order, Quotation
from users.models import Address
from checkoutdetails.signals import quotation_status_changed
from location.models import CityCountryServiceProvider, CountryCode
from api.v1.serializers.products import (
    ParcelSerializer,
    PackageSerializer,
    ContainerSerializer,
)


class DeyaratContactCompanySerializer(WritableNestedModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = DeyaratContactCompany
        fields = ("id", "name", "address")


class DeyaratContactSerializer(WritableNestedModelSerializer):
    """
    Serializer for deyarat contact
    """

    address = AddressSerializer()
    company = DeyaratContactCompanySerializer(source="contact_company")

    class Meta:
        model = DeyaratContact
        fields = (
            "id",
            "contact_type",
            "first_name",
            "last_name",
            "email",
            "address",
            "company",
        )


class OrderCheckoutSerializer(WritableNestedModelSerializer):
    """
    Serializer for checkout page
    """
    consignor_contact = DeyaratContactSerializer()
    delivery_contact = DeyaratContactSerializer()
    consignee_contact = DeyaratContactSerializer()
    quotation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=True,
        queryset=Quotation.objects.all(),
        source="win_quotation",
    )

    class Meta:
        model = Order
        fields = (
            "consignor_contact",
            "delivery_contact",
            "consignee_contact",
            "quotation_id",
        )

    def update(self, instance, validated_data):
        with transaction.atomic():
            win_quotation = validated_data["win_quotation"]
            win_quotation.status = Quotation.STATUS.APPROVED
            win_quotation.save()
            instance = super().update(instance, validated_data)
            quotation_status_changed.send(sender=Quotation, quotation=win_quotation, payment_transaction=None)

        return instance


class QuotationPaymentInfoSerializer(serializers.ModelSerializer):
    total_cost = serializers.DecimalField(decimal_places=2, max_digits=10,
                                          read_only=True)

    class Meta:
        model = Quotation
        fields = (
            "total_cost",
        )


class OrderPaymentInfoSerializer(WritableNestedModelSerializer):
    """
    Serializer for payment info page
    """
    company_billing_address = DeyaratContactCompanySerializer()
    win_quotation = QuotationPaymentInfoSerializer()

    class Meta:
        model = Order
        fields = (
            "company_billing_address",
            "win_quotation",
        )


class CountryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryCode
        fields = "__all__"


class CityCountryServiceProviderSerializer(serializers.ModelSerializer):
    country = CountryCodeSerializer()

    class Meta:
        model = CityCountryServiceProvider
        fields = "__all__"


class InvoiceOrderSerializer(serializers.ModelSerializer):
    parcels = ParcelSerializer(many=True)
    packages = PackageSerializer(many=True)
    containers = ContainerSerializer(many=True)
    origin_city = CityCountryServiceProviderSerializer()
    destination_city = CityCountryServiceProviderSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class InvoiceQuotationSerializer(serializers.ModelSerializer):
    order = InvoiceOrderSerializer()
    company_name = serializers.CharField(source="carrier.company.name", read_only=True)
    carrier_full_name = serializers.CharField(
        source="carrier.get_full_name", read_only=True
    )

    class Meta:
        model = Quotation
        fields = "__all__"


class InvoicesListSerializer(serializers.ModelSerializer):
    quotation = InvoiceQuotationSerializer()

    class Meta:
        model = Invoice
        fields = "__all__"
