from django.urls import path
from .views import (
    CategoryListView, 
    PaginatedProductsView, 
    ProductDetailView, 
    InventoryListView, 
    ProductCreateView,
    ProductView,
    StockView
)

urlpatterns = [
    path('category/', CategoryListView),
    path('products/', PaginatedProductsView.as_view()),
    path('product/<uuid:id>/<slug:slug>', ProductDetailView.as_view()),
    path('inventory/products', InventoryListView.as_view()),
    path('inventory/product/create', ProductCreateView.as_view()),
    path('inventory/product/<uuid:id>/<slug:slug>', ProductView.as_view()),
    path('inventory/product/stock/<uuid:id>/<slug:slug>', StockView.as_view()),
]