from celery import shared_task
from rest_framework import serializers

@shared_task
def stock(product, amount):
    if amount != 0:
        product.stock += amount
        product.save()
        return product
    raise serializers.ValidationError({'detail': 'La cantidad debe ser mayor a 0.'})