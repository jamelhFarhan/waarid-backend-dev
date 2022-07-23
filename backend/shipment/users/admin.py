# Django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
# third party
from allauth.socialaccount.models import (
    SocialAccount, EmailAddress, SocialToken
)
from allauth.socialaccount.models import SocialApp
from rest_framework.authtoken.models import TokenProxy
# apps
from .models import Address, CustomUser, Company


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'city', 'street', 'house', 'shipment',
                    'phone_number', 'postal_code')
    list_display_links = ('country', 'city', 'street', 'house', 'phone_number',
                          'postal_code')
    list_filter = ('country',)
    date_hierarchy = 'created_at'


class AddressInline(admin.TabularInline):
    model = Address


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'get_account_type', 'website',)
    list_display_links = ('name', 'owner')

    def get_account_type(self, obj):
        return obj.get_account_type_display()


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role', 'email', 'is_admin',
                    'get_full_name', 'get_company_name',)
    list_display_links = ('username', 'email')
    search_fields = ('username', 'email',)
    list_filter = ('role',)
    date_hierarchy = 'created_at'
    readonly_fields = ('get_company_name', )

    fieldsets = (
        ('Personal info', {'fields': (
            'first_name',
            'last_name',
            'role',
            'email',
            'username',
            'avatar',
            'address',
            'get_company_name',
        )}),
        ('Permissions', {'fields': (
            'is_active', 'is_valid', 'is_admin', 'is_staff',
        )}),
    )

    def save_form(self, request, form, change):
        """
        Delete token after approving carrier.
        """
        try:
            user_email = request.POST["email"]
            user = CustomUser.objects.get(email=user_email)
            previous_role = user.role
            next_role = int(request.POST["role"])
            if (
                previous_role == CustomUser.ROLE.REQUEST_CARRIER
                and next_role == CustomUser.ROLE.CARRIER
            ):
                user.auth_token.delete()
        except ObjectDoesNotExist:
            pass
        return super().save_form(request, form, change)

    def get_company_name(self, obj):
        if obj.company:
            return obj.company.name
        return None

    get_company_name.short_description = 'Company name'


# Register your models here.
admin.site.register(Address, AddressAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Company, CompanyAdmin)
# unregister unnesessary models
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)
# admin.site.unregister(EmailAddress)
admin.site.unregister(TokenProxy)

admin.site.site_header = 'Deyarat'
