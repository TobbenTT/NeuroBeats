from django.shortcuts import render
from .models import Song
# Create your views here.

def home(request):
    # 1 Obtener Todas las Cansiones de la BD
    songs = Song.objects.all().order_by('-created_at')

    # 2 Entregarlas al template Home
    return render(request, 'home.html', {'songs': songs})