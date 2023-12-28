from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ExportMixin
from import_export.formats import base_formats

from products.models import ProductCategory, Product, Basket

admin.site.register(ProductCategory)

class ProductResource(resources.ModelResource):
    id = fields.Field(column_name='ID', attribute='id')
    name = fields.Field(column_name='title', attribute='name')    
    description = fields.Field(column_name='description', attribute='description')
    price = fields.Field(column_name='price', attribute='price')    
    quantity = fields.Field(column_name='quantity', attribute='quantity')
    category = fields.Field(column_name='category', attribute='category')
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'category')
        export_order = ('id', 'name', 'description', 'price', 'quantity', 'category')        
        batch_size = 50

    def get_export_queryset(self, queryset):
        return queryset.filter(price__gt=1900)

    def dehydrate_price(self, product):
        return f"{product.price} руб"

    def get_queryset(self):    
        return Product.objects.order_by('id')
    
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