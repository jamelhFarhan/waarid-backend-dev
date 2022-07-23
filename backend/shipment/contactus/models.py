from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField(max_length=1000)

    class Meta:
        verbose_name = _('Contact Us Message')
        verbose_name_plural = _('Contact Us Messages')
