from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from users.models import Address
from orders.models import Order, Quotation
from payment.models import PaymentTransaction
from checkoutdetails.utils import StatusChoice


class DeyaratContactCompany(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=50)
    tax_id = models.CharField(_('Tax ID'), max_length=30, default='',
                              blank=True, null=True)
    address = models.OneToOneField(
        Address,
        verbose_name=_("Address"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.name}"


class DeyaratContact(TimeStampedModel):
    CONSIGNOR = 1
    DELIVERY = 2
    CONSIGNEE = 3
    CONTACT_TYPE_CHOICES = (
        (CONSIGNOR, "Consignor"),
        (DELIVERY, "Delivery"),
        (CONSIGNEE, "Consignee"),
    )

    contact_type = models.IntegerField(
        _("Contact Type"),
        choices=CONTACT_TYPE_CHOICES,
        db_index=True,
        null=True,
    )
    first_name = models.CharField(_("First name"), max_length=50,
                                  null=True, blank=True)
    last_name = models.CharField(_("Last name"), max_length=50,
                                 null=True, blank=True)
    email = models.EmailField(
        verbose_name=_("Email address"),
        max_length=255,
    )
    address = models.ForeignKey(
        Address,
        verbose_name=_("Address"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    contact_company = models.ForeignKey(
        DeyaratContactCompany,
        verbose_name=_("Company"),
        null=True,
        on_delete=models.SET_NULL,
    )


class Booking(TimeStampedModel):
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.CASCADE, related_name='bookings')

    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')


class Invoice(TimeStampedModel):
    quotation = models.ForeignKey(Quotation, verbose_name=_("Quotation"), on_delete=models.CASCADE,
                                  related_name="invoices")
    status = models.IntegerField(_('Status'), choices=StatusChoice.choices(), default=0)  # get from Quotation status
    booking = models.ForeignKey(Booking, verbose_name=_("Booking"), on_delete=models.CASCADE, related_name="invoices")
    payment_transaction = models.ForeignKey(PaymentTransaction, verbose_name=_("Payment Transaction"),
                                            on_delete=models.SET_NULL, related_name="invoices", null=True, blank=True)

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')

