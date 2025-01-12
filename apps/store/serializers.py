from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate(self, attrs):
        return super().validate(attrs)

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        required=False
    ) # Solo escritura, osea solo el post y el put
    category_name = serializers.CharField(
        source='category.name', 
        read_only=True
    ) # Solo lectura, osea solo el get

    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'slug', 
            'description', 
            'image', 
            'price', 
            'is_sale', 
            'discount_percentage', 
            'discounted_price', 
            'stock', 
            'category', 
            'category_name'
        ]
        extra_kwargs = {
            'name': {'required': False}
        }
        
    def create(self, validated_data):
        try:
            product = Product.objects.create(**validated_data)
            return product
        except Exception as e:
            raise serializers.ValidationError({'detail': f'Error al crear el producto: {str(e)}'})
        
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['stock']