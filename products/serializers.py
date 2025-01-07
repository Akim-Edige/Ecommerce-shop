from rest_framework import fields, serializers

from products.models import Basket, Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price', 'image', 'description', 'quantity')


class BasketAddUpdateSeriaizer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='id', queryset=Product.objects.all())

    class Meta:
        model = Basket
        fields = ("product",)


class BasketViewSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    # user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    sum = fields.FloatField()
    total_price = fields.SerializerMethodField()
    total_count = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('user', 'product', 'quantity', 'sum', 'total_price', 'total_count', 'created_timestamp')
        read_only_fields = ('created_timestamp', 'sum')

    @classmethod
    def get_total_price(cls, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_price()

    @classmethod
    def get_total_count(cls, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_count()
