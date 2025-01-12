import random
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()

@shared_task
def send_verification_email(email, url):
    """
    Se enviara un correo con la url y el codigo para verificar el email que ingreso el usuario.
    """
    host = settings.HOST

    code = random.randint(100000000, 999999999)
    cache_key = f'verificacion_email_{code}'
    cache.set(cache_key, email, timeout=600)

    subject = 'Verificación de email'
    message = f'Por favor verifique su email ingresando este codigo: {code} en esta pagina: {host}/api/{url}'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )

@shared_task
def account_not_verify():
    """
    Tarea periodica la cual se ejecutara cada 10 minutos, para 
    eliminar cuentas que han sido creadas pero el usuario no las a verificado.
    """
    time_limit = now() - timedelta(minutes=10)
    del_user = User.objects.filter(is_email_verified=False, date_joined__lte=time_limit)
    
    for user in del_user:
        user.delete()