from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class PaymentTransaction(TimeStampedModel):
    status = models.CharField(_("status"), max_length=128)
    response_code = models.CharField(_("response code"), max_length=128)

    class Meta:
        verbose_name = _('Payment transaction')
        verbose_name_plural = _('Payment transactions')
