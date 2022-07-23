# django
from django.db import models
from django.utils.translation import gettext_lazy as _

# applications
from utils.mixins import DateTimeMixin
from users.models import CustomUser


class ServiceProvider(DateTimeMixin):
    """
    Service provider like - "DHL", "Aramex", ...
    """
    name = models.CharField(_('name'), max_length=128, unique=True)
    user = models.OneToOneField(CustomUser, verbose_name=_('User'), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('Service Provider')
        verbose_name_plural = _('Service Providers')


class CountryCode(DateTimeMixin):
    """
    Country code with full name of country and service that supports them
    """
    country_code = models.CharField(_('Country code'), max_length=2, unique=True)
    country_name = models.CharField(_('Country name'), max_length=128)
    service_provider = models.ManyToManyField(ServiceProvider, related_name='countries')
    active = models.BooleanField(_("Active"), default=True)
    priority = models.IntegerField(_("Priority"), default=0)

    class Meta:
        verbose_name = _('Country Code')
        verbose_name_plural = _('Country Codes')

    def __str__(self):
        return self.country_name


class CityCountryServiceProvider(DateTimeMixin):
    """
    City that is bounded to CountryCode and ServiceProvider
    """
    service_provider = models.ManyToManyField(ServiceProvider, related_name='cities')
    country = models.ForeignKey(CountryCode, related_name='cities', on_delete=models.CharField)  # Foreignkey to CountryCode
    city_name = models.CharField(_('City name'), max_length=128)
    active = models.BooleanField(_("Active"), default=True)
    post_code1 = models.CharField(_('Post Code1'), max_length=100, null=True, blank=True)
    post_code2 = models.CharField(_('Post Code2'), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('City with Country and Service Provider')
        verbose_name_plural = _('Cities with Countries and Service Providers')
        unique_together = ['country', 'city_name']

    def __str__(self):
        return '{}, {}'.format(self.city_name, self.country)
