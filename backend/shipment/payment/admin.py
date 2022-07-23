from django.contrib import admin

from payment.models import PaymentTransaction


class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'response_code', 'created', 'modified')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
