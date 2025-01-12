from rest_framework import serializers
from .models import ShippingAddress

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            'id', 
            'full_name', 
            'email', 
            'phone', 
            'address', 
            'country', 
            'state', 
            'city', 
            'zipcode', 
            'is_default'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'full_name': {'required': False},
            'email': {'required': False},
            'phone': {'required': False},
            'address': {'required': False},
            'country': {'required': False},
            'state': {'required': False},
            'city': {'required': False},
            'zipcode': {'required': False}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        return ShippingAddress.create_address(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class GuestShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name', 
            'email', 
            'phone', 
            'address', 
            'country', 
            'state', 
            'city', 
            'zipcode'
        ]