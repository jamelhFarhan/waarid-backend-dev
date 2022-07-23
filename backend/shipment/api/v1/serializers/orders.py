from collections.abc import Mapping
from collections import OrderedDict
# import json

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework.fields import get_error_detail, SkipField, set_value
from rest_framework.relations import PKOnlyObject

from django.core.exceptions import ValidationError as DjangoValidationError

from orders.models import Order, Quotation, Note
from users.models import Address, CustomUser
from products.models import Parcel, Package, Container
from utils.records import create_contact
from api.v1.serializers.products import (
    ParcelSerializer, PackageSerializer, ContainerSerializer
)
from api.v1.serializers.users import AddressSerializer, CustomUserSerializer
from location.serializers import CityCountrySerializer
from tarif_breakdown.serializers import (
    OriginAddressChargesSerializer,
    OriginChargesSerializer,
    PortToPortChargesSerializer,
    DestinationChargesSerializer,
    DestinationAddressChargesSerializer,
    CustomsBrokerageChargesSerializer,
    InsuranceChargesSerializer,
)


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for notes
    """
    role = serializers.IntegerField(source='owner.role', read_only=True)
    quotation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        queryset=Quotation.objects.all(),
        source="quotation",
    )

    class Meta:
        model = Note
        fields = ('id', 'text', 'owner', 'role', 'quotation_id', 'created_at', )

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.get_full_name()
        return representation


class QuotationSerializer(WritableNestedModelSerializer):
    """
    Serializer for Quotations
    """
    carrier_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=True,
        queryset=CustomUser.objects.all(),
        source="carrier",
    )
    order_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=True,
        queryset=Order.objects.all(),
        source="order",
    )
    company_name = serializers.CharField(source='carrier.company.name',
                                         read_only=True)
    carrier_full_name = serializers.CharField(source='carrier.get_full_name',
                                              read_only=True)
    shipment_origin = serializers.CharField(source='order.shipment_origin',
                                            read_only=True)
    shipment_destination = serializers.CharField(
        source='order.shipment_destination', read_only=True)
    cargo_ready_date = serializers.CharField(source='order.cargo_ready_date',
                                             read_only=True)
    origin_city = CityCountrySerializer(source='order.origin_city',
                                        read_only=True)
    destination_city = CityCountrySerializer(source='order.destination_city',
                                             read_only=True)
    transport_mode = serializers.IntegerField(source='order.transport_mode',
                                           read_only=True)
    unit_system = serializers.IntegerField(source='order.unit_system',
                                        read_only=True)
    description = serializers.CharField(source='order.description',
                                        read_only=True)
    parcels = serializers.SerializerMethodField()
    packages = serializers.SerializerMethodField()
    containers = serializers.SerializerMethodField()

    notes = NoteSerializer(many=True, read_only=False)

    origin_address_charges = OriginAddressChargesSerializer(many=True, read_only=False)
    origin_charges = OriginChargesSerializer(many=True, read_only=False)
    port_to_port_charges = PortToPortChargesSerializer(many=True, read_only=False)
    destination_charges = DestinationChargesSerializer(many=True, read_only=False)
    destination_address_charges = DestinationAddressChargesSerializer(many=True, read_only=False)
    customs_brokerage_charges = CustomsBrokerageChargesSerializer(many=True, read_only=False)
    insurance_charges = InsuranceChargesSerializer(many=True, read_only=False)

    class Meta:
        model = Quotation
        fields = ('id', 'carrier_id', 'company_name', 'order_id', 'total_cost',
                  'currency', 'eta', 'valid_till_date', 'status',
                  'carrier_full_name', 'shipment_origin', 'origin_city',
                  'shipment_destination', 'destination_city', 'cargo_ready_date', 'transport_mode',
                  'parcels', 'packages', 'containers', 'unit_system',
                  'description', 'notes', 'origin_address_charges', 'origin_charges',
                  'port_to_port_charges', 'destination_charges', 'destination_address_charges',
                  'customs_brokerage_charges', 'insurance_charges', 'remarks',
        )

    def get_parcels(self, obj):
        parcels = list(obj.order.parcels.values())
        return parcels

    def get_packages(self, obj):
        parcels = list(obj.order.packages.values())
        return parcels

    def get_containers(self, obj):
        parcels = list(obj.order.containers.values())
        return parcels

    def to_representation(self, instance):
        """
        this is temp workaround for carriers getting
        only own quotations on manage requests page.
        """
        user = self.context['request'].user
        if user.role == CustomUser.ROLE.CARRIER:
            if instance.carrier != user:
                return None
        return super().to_representation(instance)


class OrderSerializer(WritableNestedModelSerializer):
    parcels = ParcelSerializer(many=True)
    packages = PackageSerializer(many=True)
    containers = ContainerSerializer(many=True)
    origin_city = CityCountrySerializer()
    destination_city = CityCountrySerializer()
    quotations = QuotationSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "origin_city",
            "destination_city",
            "description",
            "cargo_ready_date",
            "transport_mode",
            "owner",
            "unit_system",
            "parcels",
            "packages",
            "containers",
            "quotations",
            "need_customs_brokerage",
            "need_insurance",
            "shipment_value",
            "item_description",
            "created_at",
        )

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = super().to_representation(instance)
        quotations = ret.get("quotations")
        if quotations:
            quotations = [quotation for quotation in quotations if quotation is not None]
            ret["quotations"] = quotations

        return ret


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for contact details page
    """
    consignor = CustomUserSerializer()
    deliveryman = CustomUserSerializer()
    consignee = CustomUserSerializer()
    quotation_id = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ('id', 'consignor', 'deliveryman', 'consignee',
                  'quotation_id',)

    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        """
        if not isinstance(data, Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')

        ret = OrderedDict()
        fields = self._writable_fields

        for field in fields:
            field_name = field.field_name
            validated_value = data.get(field_name)
            set_value(ret, field.source_attrs, validated_value)

        return ret

    def update(self, instance, validated_data):
        for attr, val in validated_data.items():
            if (attr == 'consignor' or attr == 'deliveryman' or attr == 'consignee') and val:
                value = create_contact(val)
                setattr(instance, attr, value)
            elif attr == 'quotation_id':
                quotation = Quotation.objects.get(id=val)
                quotation.status = Quotation.STATUS.APPROVED
                quotation.save()
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields
        print(ret)
        for field in fields:
            if field.field_name == 'quotation_id':
                attribute = instance.quotations.get(status=Quotation.STATUS.APPROVED).id
            else:
                try:
                    attribute = field.get_attribute(instance)
                except SkipField:
                    continue

            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)
        return ret
