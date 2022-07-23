from rest_framework import serializers

from orders.models import Quotation
from tarif_breakdown.models import (
    OriginAddressCharges,
    OriginCharges,
    PortToPortCharges,
    DestinationCharges,
    DestinationAddressCharges,
    CustomsBrokerageCharges,
    InsuranceCharges,
)


class OriginAddressChargesSerializer(serializers.ModelSerializer):
    """
    Serializer for OriginAddressCharges
    """

    quotation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        queryset=Quotation.objects.all(),
        source="quotation",
    )

    class Meta:
        model = OriginAddressCharges
        fields = (
            "id",
            "fee_code",
            "fee_name",
            "comment",
            "units",
            "quotation_id",
            "unit_price",
            "amount",
        )


class OriginChargesSerializer(serializers.ModelSerializer):
    """
    Serializer for OriginCharges
    """

    quotation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        queryset=Quotation.objects.all(),
        source="quotation",
    )

    class Meta:
        model = OriginCharges
        fields = (
            "id",
            "fee_code",
            "fee_name",
            "comment",
            "units",
            "quotation_id",
            "unit_price",
            "amount",
        )


class PortToPortChargesSerializer(serializers.ModelSerializer):
    """
    Serializer for PortToPortCharges
    """

    quotation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        queryset=Quotation.objects.all(),
        source="quotation",
    )

    class Meta:
        model = PortToPortCharges
        fields = (
            "id",
            "fee_code",
            "fee_name",
            "comment",
            "units",
            "quotation_id",
            "unit_price",
            "amount",
        )


class DestinationChargesSerializer(serializers.ModelSerializer):
    """
    Serializer for DestinationCharges
    """

    quotation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        queryset=Quotation.objects.all(),
        source="quotation",
    )

    class Meta:
        model = DestinationCharges
        fields = (
            "id",
            "fee_code",
            "fee_name",
            "comment",
            "units",
            "quotation_id",
            "unit_price",
            "amount",
        )


class DestinationAddressChargesSerializer(serializers.ModelSerializer):
    """
    Serializer for DestinationAddressCharges
    """

    quotation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        queryset=Quotation.objects.all(),
        source="quotation",
    )

    class Meta:
        model = DestinationAddressCharges
        fields = (
            "id",
            "fee_code",
            "fee_name",
            "comment",
            "units",
            "quotation_id",
            "unit_price",
            "amount",
        )


class CustomsBrokerageChargesSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomsBrokerageCharges
    """

    quotation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        queryset=Quotation.objects.all(),
        source="quotation",
    )

    class Meta:
        model = CustomsBrokerageCharges
        fields = (
            "id",
            "fee_name",
            "comment",
            "amount",
            "quotation_id",
        )


class InsuranceChargesSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomsBrokerageCharges
    """

    quotation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        queryset=Quotation.objects.all(),
        source="quotation",
    )

    class Meta:
        model = InsuranceCharges
        fields = (
            "id",
            "fee_name",
            "comment",
            "amount",
            "quotation_id",
        )
