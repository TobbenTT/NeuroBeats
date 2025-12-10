from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Badge

# Register your models here.

# 1. Personalización del Admin de Usuario
admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')

admin.site.register(User, CustomUserAdmin)

# 2. Personalización del Admin de Perfil
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_last_login', 'is_private')
    readonly_fields = ('get_last_login',)

    def get_last_login(self, obj):
        return obj.user.last_login
    get_last_login.short_description = 'Última Conexión'
    get_last_login.admin_order_field = 'user__last_login'

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Badge)