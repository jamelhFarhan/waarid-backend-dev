from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from currency.utils import MainCurrencyException, CurrencyNameException


class Currency(models.Model):
    name = models.CharField(_("Name"), max_length=3, unique=True)
    active = models.BooleanField(_("Active"), default=True)
    main = models.BooleanField(_("Main"), default=False)

    def save(self, *args, **kwargs):
        currency_class = self.__class__
        self.name = self.name.upper()

        if not self.id:
            if self.main is True and currency_class.objects.filter(main=True):
                raise MainCurrencyException("Only one main currency is allowed")

            if currency_class.objects.filter(name=self.name):
                raise CurrencyNameException(f"Currency with name {self.name} already exists")
        else:
            if self.main is True and currency_class.objects.filter(~Q(pk=self.id), main=True):
                raise MainCurrencyException("Only one main currency is allowed")

            if currency_class.objects.filter(~Q(pk=self.id), name=self.name):
                raise CurrencyNameException(f"Currency with name {self.name} already exists")

        super().save(*args, **kwargs)

    @classmethod
    def set_main(cls, pk: int, main: bool = True):
        """
        Set currency by pk as main currency
        """
        if main and cls.objects.filter(~Q(pk=pk), main=True):
            raise MainCurrencyException("Allowed only one main currency")

        cls.objects.filter(pk=pk).update(main=main)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


class CurrencyRate(models.Model):
    rate = models.DecimalField(_("Rate"), max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, verbose_name=_("Currency"), on_delete=models.CASCADE,
                                 related_name="currency_rates")
    date = models.DateField(_("Date"), auto_now=True)

    class Meta:
        verbose_name = _('Currency Rate')
        verbose_name_plural = _('Currency Rates')
        ordering = ["-date"]

