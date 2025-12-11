from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Badge

# Register your models here.

# 1. Personalización del Admin de Usuario
admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_status')

    def get_status(self, obj):
        from django.utils import timezone
        import datetime
        from django.utils.timesince import timesince

        # Acceder al perfil de forma segura
        profile = getattr(obj, 'profile', None)
        if not profile or not profile.last_activity:
            return "⚪ Desconocido"

        now = timezone.now()
        diff = now - profile.last_activity

        if diff < datetime.timedelta(minutes=5):
            return "🟢 Online"
        else:
            return f"🔴 Hace {timesince(profile.last_activity).split(',')[0]}"
    
    get_status.short_description = 'Estado'

admin.site.register(User, CustomUserAdmin)

# 2. Personalización del Admin de Perfil
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_status', 'is_private')
    readonly_fields = ('get_last_login', 'last_activity')

    def get_last_login(self, obj):
        return obj.user.last_login
    get_last_login.short_description = 'Última Conexión'
    get_last_login.admin_order_field = 'user__last_login'

    def get_status(self, obj):
        from django.utils import timezone
        import datetime

        if not obj.last_activity:
            return "⚪ Desconocido"

        # Definir umbral de 5 minutos para "Online"
        now = timezone.now()
        diff = now - obj.last_activity

        if diff < datetime.timedelta(minutes=5):
            return "🟢 Online"
        else:
            # Calcular tiempo transcurrido
            from django.utils.timesince import timesince
            return f"🔴 Hace {timesince(obj.last_activity).split(',')[0]}"
            
    get_status.short_description = 'Estado'
    get_status.admin_order_field = 'last_activity'

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Badge)