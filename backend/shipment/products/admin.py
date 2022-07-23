from django.contrib import admin

from products.models import Parcel, Package, Container


class ParcelAdmin(admin.ModelAdmin):
    list_display = ('id', 'parcel_type', 'weight', 'created_at')
    list_display_links = ('id', 'parcel_type', 'weight',)
    list_filter = ('parcel_type',)


class ParcelInline(admin.TabularInline):
    model = Parcel
    extra = 0


class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'package_type', 'weight', 'length', 'height',
                    'width', 'quantity', 'stackable', 'created_at')
    list_display_links = ('id', 'package_type', 'weight', 'quantity',
                          'stackable', 'created_at')
    list_filter = ('package_type',)


class PackageInline(admin.TabularInline):
    model = Package
    extra = 0


class ContainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'container_type', 'cross_weight', 'quantity',
                    'overweight', 'created_at')
    list_display_links = ('container_type', 'cross_weight', 'quantity',
                          'overweight', 'created_at')
    list_filter = ('container_type',)


class ContainerInline(admin.TabularInline):
    model = Container
    extra = 0


# Register your models here.
# admin.site.register(Parcel, ParcelAdmin)
# admin.site.register(Package)
# admin.site.register(Container)
