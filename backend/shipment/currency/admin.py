from django.contrib import admin

from currency.models import Currency, CurrencyRate
from currency.utils import MainCurrencyException, CurrencyNameException
from django.contrib import messages


class CurrencyInline(admin.TabularInline):
    model = Currency


class CurrencyRateInline(admin.TabularInline):
    # raw_id_fields = ("name",)
    model = CurrencyRate
    extra = 1


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active", "main")
    inlines = (CurrencyRateInline,)

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except (MainCurrencyException, CurrencyNameException) as e:
            messages.add_message(request, messages.ERROR, str(e))


admin.site.register(Currency, CurrencyAdmin)


class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ("id", "rate", "currency", "date")
    # inlines = (CurrencyInline,)


admin.site.register(CurrencyRate, CurrencyRateAdmin)
