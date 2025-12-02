from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from music.models import Song
from .forms import ProfileUpdateForm

@login_required
def profile(request):
    # 1. Obtener las canciones que el usuario ha subido
    my_songs = Song.objects.filter(uploader=request.user).order_by('-created_at')
    
    # 2. Pasar datos al template
    return render(request, 'profile.html', {
        'my_songs': my_songs
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'edit_profile.html', {'form': form})