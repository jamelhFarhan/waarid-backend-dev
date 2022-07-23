from django.db.models.signals import post_save
from django.dispatch import receiver


from .tasks import aramex_quote, dhl_quote
from .models import Order

@receiver(post_save, sender=Order)
def aramex_create_quote(sender, instance, created, *args, **kwargs):
    if instance and created:
        aramex_quote.apply_async((instance.id,))
        dhl_quote.apply_async((instance.id,))
