from collections.abc import Mapping
from collections import OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework.fields import get_error_detail, SkipField, set_value

from django.core.exceptions import ValidationError as DjangoValidationError

from products.models import Parcel, Package, Container


class ParcelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parcel
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = '__all__'


class ContainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Container
        fields = '__all__'

