from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from music.models import Song
from .forms import ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import logout

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

# Esta función verifica si el usuario es "Superusuario" (Admin)
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)  # <--- CANDADO DE SEGURIDAD 🔒
def create_user_fast(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Usuario {username} creado con éxito!')
            return redirect('profile') # Te devuelve a tu perfil
    else:
        form = UserCreationForm()
    
    return render(request, 'create_user.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('login')  # Nos manda a la página de inicio de sesión