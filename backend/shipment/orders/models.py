# django
from django.db import models
from django.utils.translation import gettext_lazy as _

# applications
from utils.mixins import DateTimeMixin
from utils.media import file_path
from users.models import Address, CustomUser
from location.models import CityCountryServiceProvider


# Create your models here.
class Order(DateTimeMixin):
    """
    Model for creating order
    """
    class STATUS(object):
        REQUEST = 1
        QUOTE = 2
        CHECKOUT = 3
        IN_PROGRESS = 4  # after payment
        SHIPPED = 5
        DELIVERED = 6
        ARCHIEVED = 7

        ALL = [QUOTE, REQUEST, CHECKOUT, IN_PROGRESS, SHIPPED, DELIVERED,
               ARCHIEVED]

        CHOICES = (
            (REQUEST, _('Request')),
            (QUOTE, _('Quote')),
            (CHECKOUT, _('Checkout')),
            (IN_PROGRESS, _('In progress')),
            (SHIPPED, _('Shipped')),
            (DELIVERED, _('Delivered')),
            (ARCHIEVED, _('Archieved')),
        )

    class MODE(object):
        SEA_FREIGHT = 1
        LAND = 2
        AIR_CARGO = 3

        ALL = [SEA_FREIGHT, LAND, AIR_CARGO]

        CHOICES = (
            (SEA_FREIGHT, _('Sea freight')),
            (LAND, _('Land')),
            (AIR_CARGO, _('Air cargo')),
        )

    class SYSTEM(object):
        METRIC = 1
        IMPERIAL = 2

        ALL = [METRIC, IMPERIAL, ]

        CHOICES = (
            (METRIC, _('Metric system')),
            (IMPERIAL, _('Imperial system')),
        )

    status = models.IntegerField(_('Order status'),
                                 choices=STATUS.CHOICES,
                                 default=STATUS.REQUEST,
                                 db_index=True)
    shipment_origin = models.OneToOneField(
        Address,
        verbose_name='shipment origin',
        related_name='shipment_origin',
        on_delete=models.SET_NULL,
        null=True,
    )
    shipment_destination = models.OneToOneField(
        Address,
        verbose_name='shipment destination',
        related_name='shipment_destination',
        on_delete=models.SET_NULL,
        null=True,
    )
    cargo_ready_date = models.DateField(_('Cargo ready date'))
    description = models.TextField(_('Description'), blank=True, null=True)
    transport_mode = models.IntegerField(_('Preferred transport mode'),
                                         choices=MODE.CHOICES,
                                         default=MODE.LAND,
                                         db_index=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    unit_system = models.IntegerField(_('System of Units'),
                                      choices=SYSTEM.CHOICES,
                                      default=SYSTEM.METRIC)
    consignor_contact = models.ForeignKey("checkoutdetails.DeyaratContact",
                                          on_delete=models.SET_NULL,
                                          related_name="consignor_orders",
                                          blank=True, null=True)
    delivery_contact = models.ForeignKey("checkoutdetails.DeyaratContact",
                                         on_delete=models.SET_NULL,
                                         related_name="delivery_orders",
                                    blank=True, null=True)
    consignee_contact = models.ForeignKey("checkoutdetails.DeyaratContact",
                                          on_delete=models.SET_NULL,
                                          related_name="consignee_orders",
                                          blank=True, null=True)
    company_billing_address = models.ForeignKey(
        "checkoutdetails.DeyaratContactCompany",
        on_delete=models.SET_NULL,
        related_name="orders",
        blank=True,
        null=True,
    )
    win_quotation = models.ForeignKey("orders.Quotation",
                                      on_delete=models.SET_NULL,
                                      related_name="booked_order",
                                      blank=True, null=True)
    origin_city = models.ForeignKey(CityCountryServiceProvider, on_delete=models.PROTECT, related_name="origin_orders" )
    destination_city = models.ForeignKey(CityCountryServiceProvider, on_delete=models.PROTECT,
                                         related_name="destination_orders")
    need_customs_brokerage = models.BooleanField(
        _("Need Customs Brokerage"), default=False
    )
    need_insurance = models.BooleanField(_("Need Insurance"), default=False)
    shipment_value = models.DecimalField(
        _("Shipment Value"), max_digits=10, decimal_places=2, default=0
    )
    item_description = models.TextField(_("Item Description"), blank=True, null=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return '{} - {}, {}'.format(
            self.origin_city, self.destination_city,
            self.cargo_ready_date)


class Quotation(DateTimeMixin):
    """
    Model for creating quotation
    """
    class TYPE(object):
        USD = 1

        ALL = [USD, ]

        CHOICES = (
            (USD, _('USD')),
        )

    class STATUS(object):
        IN_PROGRESS = 1
        APPROVED = 2
        EXPIRED = 3
        PAYED = 4

        ALL = [IN_PROGRESS, APPROVED, EXPIRED, PAYED, ]

        CHOICES = (
            (IN_PROGRESS, _('In progress')),
            (APPROVED, _('Approved')),
            (EXPIRED, _('Expired')),
            (PAYED, _('Payed')),
        )
    carrier = models.ForeignKey(CustomUser, verbose_name=_('Carrier'),
                                on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name=_('Quotation'),
                              related_name=_('quotations'),
                              on_delete=models.CASCADE)
    total_cost = models.DecimalField(_('Total cost'), max_digits=10,
                                     decimal_places=2, default=0)
    currency = models.IntegerField(_('Currency'), choices=TYPE.CHOICES,
                                   default=TYPE.USD)
    eta = models.DateField(_('Estimated time of arrival'), null=True,
                           blank=True)
    valid_till_date = models.DateField(_('Valid till date'), null=True,
                                       blank=True)
    status = models.IntegerField(_('Status'), choices=STATUS.CHOICES,
                                 default=STATUS.IN_PROGRESS)
    rates_file = models.FileField(_('File rates'), upload_to=file_path,
                                  blank=True, null=True)
    remarks = models.TextField(_('Remarks'), blank=True, null=True)

    class Meta:
        verbose_name = _('Quotation')
        verbose_name_plural = _('Quotations')

    def __str__(self):
        return f'{self.carrier} {self.total_cost}'

    def save(self, *args, **kwargs):
        if self.order.status == Order.STATUS.REQUEST:
            self.order.status = Order.STATUS.QUOTE
        self.order.save()
        super().save(*args, **kwargs)


class Note(DateTimeMixin):
    """
    Model for notes between customer and carrier
    """
    text = models.TextField(_('Text'))
    owner = models.ForeignKey(CustomUser, verbose_name=_('Owner'),
                              on_delete=models.CASCADE)
    quotation = models.ForeignKey(Quotation, verbose_name=_('Quotation'),
                                  related_name='notes',
                                  on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')

    def __str__(self):
        return f'{self.owner} {self.created_at}'
