from django.contrib import admin
from .models import Product, Category, Section, City

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'date',
        'section',
        'is_presale',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
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
admin.site.register(Section, SectionAdmin)
admin.site.register(City, CityAdmin)
