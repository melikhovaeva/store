from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from import_export.formats import base_formats

from products.models import ProductCategory, Product, Basket

admin.site.register(ProductCategory)

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantity', 'category')

    def get_export_queryset(self, queryset):
        return queryset.filter(price__gte=2000)

    def dehydrate_price(self, product):
        return f"${product.price}"

    def get_price(self, value):
        return float(value.replace('rub', '').replace(',', ''))
    
class BasketResource(resources.ModelResource):
    class Meta:
        model = Basket
        fields = ('product', 'quantity', 'created_timestamp')

@admin.register(Product)
class ProductAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('image', 'name', 'description', ('price', 'quantity'), 'category')
    readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('-name',)
    resource_class = ProductResource


class BasketAdmin(ExportMixin, admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
    resource_class = BasketResource