from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection

# class CollectionSerializers(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()

# class ProductSerializers(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6,decimal_places=2, source='unit_price')    
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset=Collection.objects.all()
#     # )
#     # collection = serializers.StringRelatedField()
#     # collection = CollectionSerializers()
#     collection = serializers.HyperlinkedRelatedField(
#         queryset = Collection.objects.all(),
#         view_name = 'collection-detail'
#     )

#     def calculate_tax(self,product:Product):
#         return product.unit_price * Decimal(1.1)


#model serializers
class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    
    products_count = serializers.IntegerField()


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug','inventory','unit_price','price_with_tax','collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)
    

    # def validate(self, data):
    #     if

    # def create(self, validated_data):
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)

