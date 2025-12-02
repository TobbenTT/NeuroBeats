from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Song
from .forms import SongForm
# Create your views here.

def home(request):
    # 1 Obtener Todas las Cansiones de la BD
    songs = Song.objects.all().order_by('-created_at')

    # 2 Entregarlas al template Home
    return render(request, 'home.html', {'songs': songs})

@login_required
def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.uploader = request.user
            song.save()
            return redirect('home')
        else:
            form = SongForm()
        
        return render(request, 'upload.html', {'form': form})