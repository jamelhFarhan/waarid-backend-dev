# django
from django.db import models
from django.utils.translation import gettext_lazy as _

# applications
from utils.mixins import DateTimeMixin
from orders.models import Order


# Create your models here.
class Parcel(DateTimeMixin):
    """
    Model for class Parcel
    """
    class TYPE(object):
        ENVELOPE = 1
        STANDART_FLYER = 2
        LARGE_FLYER = 3

        ALL = [ENVELOPE, STANDART_FLYER, LARGE_FLYER]

        CHOICES = (
            (ENVELOPE, _('Envelope')),
            (STANDART_FLYER, _('Standart Flyer')),
            (LARGE_FLYER, _('Large Flyer')),
        )
    parcel_type = models.IntegerField(_('Parcel type'),
                                      choices=TYPE.CHOICES,
                                      default=TYPE.ENVELOPE,
                                      db_index=True)
    weight = models.FloatField(_('Weight'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True,
                              related_name='parcels')

    def __str__(self):
        return f'{self.get_parcel_type_display()} {self.weight}'


class Package(DateTimeMixin):
    """
    Model for class Package
    """
    class TYPE(object):
        BOX = 1
        PALLET = 2
        LOAD = 3

        ALL = [BOX, PALLET, LOAD]

        CHOICES = (
            (BOX, _('Box')),
            (PALLET, _('Pallet')),
            (LOAD, _('Load')),
        )
    package_type = models.IntegerField(_('Package type'),
                                       choices=TYPE.CHOICES,
                                       default=TYPE.BOX,
                                       db_index=True)
    weight = models.FloatField(_('Weight'))
    height = models.IntegerField(_('Height'), null=True, blank=True)
    width = models.IntegerField(_('Width'), null=True, blank=True)
    length = models.IntegerField(_('Length'), null=True, blank=True)
    quantity = models.IntegerField(_('Quantity'), default=1)
    stackable = models.BooleanField(_('Stackable'), default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True,
                              related_name='packages')
    volume = models.IntegerField(_('Volume'), null=True, blank=True)

    def __str__(self):
        return f'{self.package_type} {self.weight}'


class Container(DateTimeMixin):
    """
    Model for class Container
    """
    class TYPE(object):
        STANDART20 = 1
        STANDART40 = 2

        ALL = [STANDART20, STANDART40]

        CHOICES = (
            (STANDART20, _('20 Standart')),
            (STANDART40, _('40 Standart')),
        )
    container_type = models.IntegerField(_('Container type'),
                                         choices=TYPE.CHOICES,
                                         default=TYPE.STANDART20,
                                         db_index=True)
    cross_weight = models.FloatField(_('Cross weight'))
    quantity = models.IntegerField(_('Quantity'), default=1)
    overweight = models.BooleanField(_('Overweight'), default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True,
                              related_name='containers')

    def __str__(self):
        return f'{self.container_type} {self.cross_weight}'
