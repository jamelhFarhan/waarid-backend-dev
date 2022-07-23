from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError

from allauth.account.adapter import get_adapter
from rest_framework import serializers
from allauth.account.utils import setup_user_email
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from dj_rest_auth.serializers import PasswordResetSerializer


from api.v1.forms.auth import CustomResetPasswordForm
from users.models import Company, Address


class CustomRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
        return email

    def validate_password1(self, password1):
        return get_adapter().clean_password(password1)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def custom_signup(self, request, user):
        pass

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )
        company_name = request.data.get('company_name')
        phone_number = request.data.get('phone_number')
        country = request.data.get('country')
        role = request.data.get('role')
        user.role = role
        account_type = 1 if role == 2 else 2
        address = Address.objects.create(country=country,
                                         phone_number=phone_number)
        user.address = address
        user.save()
        if company_name:
            Company.objects.create(name=company_name, owner=user,
                                   account_type=account_type)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class CustomPasswordResetSerializer(PasswordResetSerializer):

    @property
    def password_reset_form_class(self):
        return CustomResetPasswordForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {
            'email_template': 'account/password_reset_email',
        }
