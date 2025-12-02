from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from music.models import Song

@login_required
def profile(request):
    # 1. Obtener las canciones que el usuario ha subido
    my_songs = Song.objects.filter(uploader=request.user).order_by('-created_at')
    
    # 2. Pasar datos al template
    return render(request, 'profile.html', {
        'my_songs': my_songs
    })