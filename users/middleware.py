from django.utils import timezone
from .models import Profile

class UpdateUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Actualizamos last_activity directamente en la base de datos para eficiencia
            # Usamos update() para evitar la sobrecarga de save() (signals, etc)
            Profile.objects.filter(user=request.user).update(last_activity=timezone.now())

        response = self.get_response(request)
        return response
