import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class ShippingAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False, null=True, blank=True)

    @classmethod
    def create_address(cls, user, **kwars):
        return cls.objects.create(user=user, **kwars)
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Si default es 'True', buscara las direcciones del usuario 
            # que esten en 'True' y las actualizara a 'False'.
            ShippingAddress.objects.filter(user=self.user, is_default=True).update(is_default=False)
        # Se guardara la nueva direccion con el default en 'True'.
        super(ShippingAddress, self).save(*args, **kwargs)

    def __str__(self):
        return f'Shipping Address - {self.full_name}'