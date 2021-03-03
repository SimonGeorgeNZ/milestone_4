from django.contrib import admin
from .models import Product, Category, Ticket, Section, City

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'country',
        'city',
        'section',
        'price',
        'date',
    )


class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class CityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(City, CityAdmin)
