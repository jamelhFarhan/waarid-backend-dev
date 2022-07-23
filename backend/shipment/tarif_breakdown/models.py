from django.db import models
from django.utils.translation import gettext_lazy as _

from orders.models import Quotation


class TarifBreakdownMixin(models.Model):
    """
    Mixin for adding fields to every origin/destination tarif breakdown
    """

    fee_code = models.CharField(_("Fee Code"), blank=True, null=True, max_length=255)
    fee_name = models.CharField(_("Fee Name"), blank=True, null=True, max_length=255)
    comment = models.CharField(_("Comment"), blank=True, null=True, max_length=255)
    units = models.IntegerField(_("Units"), default=1)
    unit_price = models.DecimalField(
        _("Unit Price"), max_digits=10, decimal_places=2, default=0
    )
    amount = models.DecimalField(
        _("Amount"), max_digits=10, decimal_places=2, default=0
    )

    class Meta:
        abstract = True


class OriginAddressCharges(TarifBreakdownMixin):
    """
    Address (Origin)>> CNSHA (Port Code)
    """

    quotation = models.ForeignKey(
        Quotation,
        verbose_name=_("Quotation"),
        related_name="origin_address_charges",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}, {}: {}".format(self.fee_code, self.fee_code, self.amount)


class OriginCharges(TarifBreakdownMixin):
    """
    Origin charges
    """

    quotation = models.ForeignKey(
        Quotation,
        verbose_name=_("Quotation"),
        related_name="origin_charges",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}, {}: {}".format(self.fee_code, self.fee_code, self.amount)


class PortToPortCharges(TarifBreakdownMixin):
    """
    CNSHA>> SAJED ( ports code)
    """

    quotation = models.ForeignKey(
        Quotation,
        verbose_name=_("Quotation"),
        related_name="port_to_port_charges",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}, {}: {}".format(self.fee_code, self.fee_code, self.amount)


class DestinationCharges(TarifBreakdownMixin):
    """
    Destination Charges
    """

    quotation = models.ForeignKey(
        Quotation,
        verbose_name=_("Quotation"),
        related_name="destination_charges",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}, {}: {}".format(self.fee_code, self.fee_code, self.amount)


class DestinationAddressCharges(TarifBreakdownMixin):
    """
    SAJED (Destination port code)>> Address
    """

    quotation = models.ForeignKey(
        Quotation,
        verbose_name=_("Quotation"),
        related_name="destination_address_charges",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}, {}: {}".format(self.fee_code, self.fee_code, self.amount)


class CustomsBrokerageCharges(models.Model):
    """
    Customs Brokerage Charges
    """

    fee_name = models.CharField(_("Fee Name"), blank=True, null=True, max_length=255)
    comment = models.CharField(_("Comment"), blank=True, null=True, max_length=255)
    amount = models.DecimalField(
        _("Amount"), max_digits=10, decimal_places=2, default=0
    )
    quotation = models.ForeignKey(
        Quotation,
        verbose_name=_("Quotation"),
        related_name="customs_brokerage_charges",
        on_delete=models.CASCADE,
    )


class InsuranceCharges(models.Model):
    """
    Insurance Charges
    """

    fee_name = models.CharField(_("Fee Name"), blank=True, null=True, max_length=255)
    comment = models.CharField(_("Comment"), blank=True, null=True, max_length=255)
    amount = models.DecimalField(
        _("Amount"), max_digits=10, decimal_places=2, default=0
    )
    quotation = models.ForeignKey(
        Quotation,
        verbose_name=_("Quotation"),
        related_name="insurance_charges",
        on_delete=models.CASCADE,
    )
