from django.dispatch import receiver
from django.dispatch import Signal

from .models import CustomUser
from allauth.account.models import EmailAddress


# Provides the arguments "request", "user", "from_email_address",
# "to_email_address"
user_email_changed = Signal()


@receiver(user_email_changed, sender=CustomUser)
def update_primary_email(
    sender,
    request,
    user,
    from_email_address,
    to_email_address,
    **kwargs
):
    primary_email = EmailAddress.objects.get(user_id=user.id, primary=True)
    primary_email.email = to_email_address
    primary_email.verified = False
    primary_email.save()
