from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from users.models import CustomUser, Address, Company
from users import signals


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "country",
            "city",
            "street",
            "house",
            "phone_number",
            "postal_code",
            "shipment",
        )


class CompanySerializer(WritableNestedModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "account_type",
            "description",
            "website",
            "tax_id",
            "owner",
            "address",
            "logo",
        )


class CustomUserSerializer(WritableNestedModelSerializer):
    address = AddressSerializer()
    company = CompanySerializer()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            "avatar",
            "is_admin",
            "address",
            "company",
            "created_at",
        )

    def update(self, instance, validated_data):
        if validated_data["email"] != instance.email:
            signals.user_email_changed.send(
                sender=CustomUser,
                request=self.context["request"],
                user=self.context["request"].user,
                from_email_address=instance.email,
                to_email_address=validated_data["email"],
            )

        return super().update(instance, validated_data)

