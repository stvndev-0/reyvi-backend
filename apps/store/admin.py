from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'category', 
        'price', 
        'is_sale', 
        'discount_percentage'
    )
    list_filter = (
        'category', 
        'is_sale'
    )