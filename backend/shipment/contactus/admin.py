from django.contrib import admin
from .models import ContactUs


class AdminContactUs(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'message')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(ContactUs, AdminContactUs)
