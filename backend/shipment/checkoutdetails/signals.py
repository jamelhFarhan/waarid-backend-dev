from django.dispatch import receiver, Signal

from checkoutdetails.models import Quotation, Invoice, Booking


quotation_status_changed = Signal()


@receiver(quotation_status_changed, sender=Quotation)
def update_quotation_status(sender, quotation, payment_transaction, **kwargs):
    if quotation.status == Quotation.STATUS.APPROVED:
        booking = Booking.objects.create(order=quotation.order)
        Invoice.objects.create(quotation=quotation, status=quotation.status, booking=booking,
                               payment_transaction=payment_transaction)
    elif quotation.status == Quotation.STATUS.PAYED:
        Invoice.objects.filter(quotation=quotation).update(status=quotation.status)
