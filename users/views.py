from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
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

def public_profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    
    # 1. Si soy yo mismo, voy a mi perfil privado
    if request.user.is_authenticated and request.user == user_obj:
        return redirect('profile')

    # 2. Verificar si lo sigo
    is_following = False
    liked_songs_ids = []
    
    if request.user.is_authenticated:
        is_following = request.user.profile.follows.filter(id=user_obj.profile.id).exists()
        liked_songs_ids = request.user.favorites.values_list('song_id', flat=True)

    # 3. LÓGICA DE PRIVACIDAD (EL CANDADO) 🔒
    # Si el perfil es privado Y (no lo sigo O no estoy logueado) -> BLOQUEADO
    is_locked = False
    if user_obj.profile.is_private and not is_following:
        is_locked = True
        songs = [] # No le mandamos canciones
    else:
        # Si es público O lo sigo -> Mostrar todo
        songs = Song.objects.filter(uploader=user_obj).order_by('-created_at')

    return render(request, 'public_profile.html', {
        'profile_user': user_obj,
        'songs': songs,
        'is_following': is_following,
        'liked_songs_ids': liked_songs_ids,
        'is_locked': is_locked  # <--- Enviamos esta variable al HTML
    })

# 3. Lógica del Botón Seguir (AJAX)
@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    my_profile = request.user.profile
    target_profile = target_user.profile
    
    # No puedes seguirte a ti mismo
    if request.user == target_user:
        return JsonResponse({'status': 'error'})

    # Lógica de Toggle
    if my_profile.follows.filter(id=target_profile.id).exists():
        my_profile.follows.remove(target_profile) # Dejar de seguir
        following = False
    else:
        my_profile.follows.add(target_profile) # Seguir
        following = True
        
    return JsonResponse({
        'following': following, 
        'followers_count': target_profile.followed_by.count()
    })