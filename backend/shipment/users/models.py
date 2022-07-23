# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# third-party
# from phonenumber_field.modelfields import PhoneNumberField

# applications
from utils.mixins import DateTimeMixin
from utils.media import avatar_path, logo_path
from managers import UserManager


class Address(DateTimeMixin):
    """
    Model for creating addresses for users and companies
    """
    country = models.CharField(_('Country'), max_length=30, null=True,
                               blank=True)
    city = models.CharField(_('City'), max_length=30, null=True, blank=True)
    street = models.CharField(_('Street'), max_length=30, null=True,
                              blank=True)
    house = models.CharField(_('House'), max_length=30, null=True, blank=True)
    # phone_number = PhoneNumberField(_('Phone number'), max_length=20,
    #                                 null=True, blank=True)
    phone_number = models.CharField(_('Phone number'), max_length=20,
                                    null=True, blank=True)
    postal_code = models.CharField(_('Postal code'), max_length=30, null=True,
                                   blank=True)
    shipment = models.CharField(_('Shipment address'), max_length=128,
                                null=True, blank=True)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        if self.shipment:
            return self.shipment
        return '{}, {}, {}, {}'.format(
            (self.country if self.country else ''),
            (self.city if self.city else ' '),
            (self.street if self.street else ' '),
            (self.house if self.house else ''),
        )


class CustomUser(AbstractBaseUser, DateTimeMixin, PermissionsMixin):
    """
    Model for creating custom user
    """
    class ROLE(object):
        CUSTOMER = 1
        REQUEST_CARRIER = 2
        CARRIER = 3

        ALL = [CUSTOMER, REQUEST_CARRIER, CARRIER]

        CHOICES = (
            (CUSTOMER, _('Customer')),
            (REQUEST_CARRIER, _('Unverified Carrier')),
            (CARRIER, _('Verified Carrier')),
        )

    username = models.CharField(_('Username'), max_length=50, unique=True)
    first_name = models.CharField(_('First name'), max_length=50, null=True,
                                  blank=True)
    last_name = models.CharField(_('Last name'), max_length=50, null=True,
                                 blank=True)
    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
    )
    role = models.IntegerField(
        _('Role'),
        choices=ROLE.CHOICES,
        default=ROLE.CUSTOMER,
        db_index=True,
    )
    avatar = models.ImageField(_('Avatar'), upload_to=avatar_path, default='',
                               blank=True)
    address = models.ForeignKey(Address, verbose_name=_('Address'), blank=True,
                                null=True, on_delete=models.SET_NULL)
    is_valid = models.BooleanField(_('Is valid'), default=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    is_admin = models.BooleanField(_('Is admin'), default=False)
    is_staff = models.BooleanField(_('Is staff'), default=False)

    objects = UserManager()

    class Meta:
        ordering = ['-id']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        # The user is identified by their email address
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        return self.username if self.username else self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm_list, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        try:
            company = self.company
            if self.role == 1:
                company.account_type = 2
            elif self.role in (2, 3):
                company.account_type = 1
            company.save()
        except Company.DoesNotExist:
            pass
        super(CustomUser, self).save(*args, **kwargs)


class Company(DateTimeMixin):
    """
    Model for creating company
    """
    class AccountType:
        SHIPPER = 1
        FORWADER = 2

        ALL = [SHIPPER, FORWADER]

        CHOICES = (
            (SHIPPER, _('Shipper')),
            (FORWADER, _('Forwader')),
        )
    name = models.CharField(_('Name'), max_length=50)
    account_type = models.IntegerField(_('Account type'),
                                       choices=AccountType.CHOICES,
                                       default=AccountType.FORWADER,
                                       db_index=True)
    website = models.CharField(_('Website'), max_length=30, default='',
                               blank=True)
    description = models.TextField(_('Company description'), default='',
                                   blank=True)
    tax_id = models.CharField(_('Tax ID'), max_length=30, default='',
                              blank=True)
    owner = models.OneToOneField(CustomUser, verbose_name='owner',
                                 on_delete=models.CASCADE)
    address = models.OneToOneField(Address, verbose_name=_('Address'),
                                   null=True, blank=True,
                                   on_delete=models.SET_NULL)
    logo = models.ImageField(_('Logotype'), upload_to=logo_path, default='',
                             blank=True)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return f'{self.name}'
