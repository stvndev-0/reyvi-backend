from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.cache import cache
from .models import UserAccount

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email']

class AccountVerificationSerializer(serializers.Serializer):
    code = serializers.CharField()
    class Meta:
        fields = ['code']

    def validate(self, attrs):
        code = int(attrs.get('code'))
        cache_key = f'verificacion_email_{code}'
        email = cache.get(cache_key)

        if not email:
            raise serializers.ValidationError('El codigo caduco.')
        
        cache.delete(cache_key)

        user = UserAccount.objects.get(email=email)
        user.is_email_verified = True
        user.save()
        return super().validate(attrs)        

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = ['email', 'password', 'is_email_verified']

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user: # Si no es correcto devolvemos un error en la petición
            raise serializers.ValidationError('Credenciales invalidas')
        if not user.is_email_verified:
            raise serializers.ValidationError('Tu email no está verificado.')
        data['user'] = user
        return data

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_email(self, value):
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este email ya está registrado.')
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError('Solo se permiten emails gmail.')
        return value

    def create(self, validated_data):
        email=validated_data['email']
        user = UserAccount.objects.create_user(
            username=email.split('@')[0], 
            email=email,
            password=validated_data['password']
        )
        return user