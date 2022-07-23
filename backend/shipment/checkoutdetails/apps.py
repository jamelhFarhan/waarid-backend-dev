from django.apps import AppConfig


class CheckoutdetailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkoutdetails'

    def ready(self):
        import checkoutdetails.signals
