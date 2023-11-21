# serializers.py
from rest_framework import serializers
from .models import ProductCategory, Product, Basket

class ProductCategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = ProductCategory
    fields = '__all__'
    
class ProductSerializer(serializers.ModelSerializer):
  category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

  class Meta:
    model = Product
    fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'category')

class BasketSerializer(serializers.ModelSerializer):
  user = serializers.StringRelatedField()
  product = ProductSerializer()

  class Meta:
    model = Basket
    fields = '__all__'
