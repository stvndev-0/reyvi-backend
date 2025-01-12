from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount

class UserAccountAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
        ('Opcionales', {'fields': ('is_email_verified',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = (
        'email',
        'username',
        'is_staff',
        'is_email_verified',
        'is_active',
    )
    ordering = ('email',)

admin.site.register(UserAccount, UserAccountAdmin)