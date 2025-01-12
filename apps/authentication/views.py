from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import Throttled, NotFound
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.core.cache import cache
from .serializers import (
    AccountSerializer,
    LoginSerializer,
    SignupSerializer,
    AccountVerificationSerializer
)
from .tasks import send_verification_email
from apps.payments.models import ShippingAddress
from apps.payments.serializers import ShippingAddressSerializer


class AccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AccountSerializer(instance=request.user)
        return Response(serializer.data)

class AccountVerificationView(APIView):
    def post(self, request):
        code = request.data['code']
        if code:
            serializer = AccountVerificationSerializer(code, data=request.data)
            
            if serializer.is_valid():
                print(serializer.data)
                return Response({'detail': 'Su cuenta se ha creado correctamente. Inicie sesión para continuar.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Codigo introducido incorrecto.'}, status=status.HTTP_400_BAD_REQUEST)

class ShippingAddressListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = ShippingAddress.objects.filter(user=request.user)
        serializer = ShippingAddressSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ShippingAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id, user):
        try:
            return ShippingAddress.objects.get(id=id, user=user)
        except ShippingAddress.DoesNotExist:
            raise NotFound(detail='La direccion de envio no existe.')
    
    def get(self, request, id):
        data = self.get_object(id, user=request.user)
        serializer = ShippingAddressSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        data = self.get_object(id, user=request.user)
        serializer = ShippingAddressSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'detail': 'Direccion actualizada.'
                }, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        data = self.get_object(id, user=request.user)
        data.delete()
        return Response({
            'detail': 'Direccion eliminada.'
            }, status=status.HTTP_200_OK
        )

class ShippingAddressCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ShippingAddressSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'detail': 'Direccion agregada exitosamente.'
                }, status=status.HTTP_200_OK
            )
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        # Obtengo la ip del usuario
        ip = request.META.get('REMOTE_ADDR')
        cache_key = f'intentos_login_{ip}' # Guardo la ip en un cache_key

        # Verifico los intentos previos
        attempts = cache.get(cache_key, 0)
        if attempts >= 5:
            raise Throttled(detail='Sobrepaso el limite de intentos. Intentalo de nuevo en 10 minutos.')
        
        # Valida datos enviados
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Reinicia el contador en caso de exito
            cache.delete(cache_key)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Haz iniciado sesion.',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        # Incrementa intentos fallidos en caso de error
        cache.set(key=cache_key, value=attempts + 1, timeout=600)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignUpView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            send_verification_email.delay(email=user.email, url='account_verifications')

            return Response({
                'message': 'Usuario creado con éxito.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Borramos de la request la información de sesión
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        # Cerramos la sesion
        logout(request)
        return Response({
            'message': 'Haz cerrado sesion exitosamente.'
            },status=status.HTTP_200_OK)