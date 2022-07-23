from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.mixins import DateTimeMixin

from shipping.utils import StatusChoice
from orders.models import Order


class Shipping(DateTimeMixin):
    status = models.IntegerField(_('Status'), choices=StatusChoice.choices(), default=StatusChoice.IN_PROGRESS)
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.CASCADE, related_name="shippings")
    tracking_number = models.CharField(_("Tracking number"), max_length=20)

    class Meta:
        verbose_name = _('Shipping')
        verbose_name_plural = _('Shippings')


class ImageShippings(DateTimeMixin):
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name="images")
    file = models.FileField(upload_to="shipping_image/%Y/%m/%d/", max_length=300)  # max_length default 100
    type_code = models.CharField(_("Type"), max_length=20)  # one of "invoice", "label" or "receipt"

    class Meta:
        verbose_name = _('Shipping Image')
        verbose_name_plural = _('Shipping Images')
