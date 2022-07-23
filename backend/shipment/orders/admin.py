from django.contrib import admin

from orders.models import Order, Quotation, Note
from products.admin import ParcelInline, PackageInline, ContainerInline


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0


class QuotationInline(admin.TabularInline):
    model = Quotation
    extra = 0


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'owner', 'created_at')
    list_display_links = ('id', 'text', 'owner', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class QuotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrier', 'order', 'total_cost', 'currency', 'eta',
                    'valid_till_date', 'status')
    list_display_links = ('id', 'carrier', 'order', 'total_cost', 'currency',
                          'eta', 'status')
    inlines = (NoteInline, )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'owner', 'origin_city',
                    'destination_city', 'cargo_ready_date',
                    'transport_mode', 'unit_system', 'created_at',)
    list_display_links = ('id', 'status', 'owner', 'origin_city',
                          'destination_city', 'cargo_ready_date',
                          'transport_mode',)
    list_filter = ('status', 'transport_mode', 'owner',)
    inlines = (ParcelInline, PackageInline, ContainerInline, QuotationInline)


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(Quotation, QuotationAdmin)
admin.site.register(Note, NoteAdmin)
