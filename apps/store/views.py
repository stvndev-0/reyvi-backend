from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .tasks import stock

class CategoryListView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaginatedProductsView(APIView):
    def get(self, request):
        queryset = Product.objects.all().order_by('-stock')
        paginator = PageNumberPagination()
        paginator.page_size = 12
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ProductDetailView(APIView):
    def get_object(self, id, slug):
        try:
            
            return Product.objects.get(id=id, slug=slug)
        except Product.DoesNotExist:
            raise NotFound(detail='Producto no encontrado.')
        
    def get(self, request, id, slug):
        data = self.get_object(id, slug)
        serializer = ProductSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductCreateView(APIView):
    permission_classes = [IsAdminUser]

    """
    Crear un nuevo producto
    """
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, id, slug):
        try:
            return Product.objects.get(id=id, slug=slug)
        except Product.DoesNotExist:
            raise NotFound(detail='Producto no encontrado.')
        
    """
    Obtiene los detalles de un producto por su id y slug
    """
        
    def get(self, request, id, slug):
        data = self.get_object(id, slug)
        serializer = ProductSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    Actualizar un producto existente por su id y slug
    """
    def put(self, request, id, slug):
        data = self.get_object(id, slug)
        serializer = ProductSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': f'El producto {data.name} ha sido editado'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Eliminar un producto por su id y slug
    """
    def delete(self, id, slug):
        data = self.get_object(id, slug)
        data.delete()
        return Response({
            'detail': f'Producto eliminado: {slug}'
            }, status=status.HTTP_200_OK
        )

class InventoryListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = Product.objects.all().order_by('-stock')
        serializer = ProductSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StockView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, id, slug):
        try:
            return Product.objects.get(id=id, slug=slug)
        except Product.DoesNotExist:
            raise NotFound(detail='Producto no encontrado.')

    """
    Añade stock a un producto existente
    """
    def post(self, request, id, slug):
        data = self.get_object(id, slug)
        stock.delay(data, amount=request.data['amount'])
        return Response({
            'detail': f'Se actualizo el stock de {data.name} a {data.stock}.'
            }, status=status.HTTP_200_OK
        )