from decimal import Decimal
from store.models import Product, Collection
from rest_framework import serializers

# The third way to write/create a serialize relationship:
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    # products_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
        # fields = '__all__' # do not use this, it is a bad practice

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = CollectionSerializer()

    # creating the serializer method field
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
