from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings 
from .models import Song, Rating, Favorite
from .forms import SongForm, CommentForm, SongEditForm

from .analysis import analyze_audio
import os
import uuid
from brain.engine import get_recommended_songs
from users.utils import check_and_award_badges
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    # 1. OBTIENE LAS RECOMENDACIONES (IA)
    recommended_songs = get_recommended_songs(request.user)
    
    # 2. OBTIENE EL RESTO (Exploración Global)
    recommended_ids = [song.id for song in recommended_songs]
    
    # --- CORRECCIÓN: El filtro debe estar ANTES del return ---
    explore_songs = Song.objects.filter(is_private=False).exclude(id__in=recommended_ids).order_by('-created_at')
    
    # 3. LIKES
    liked_songs_ids = []
    if request.user.is_authenticated:
        liked_songs_ids = request.user.favorites.values_list('song_id', flat=True)
    
    return render(request, 'home.html', {
        'recommended_songs': recommended_songs,
        'explore_songs': explore_songs,
        'liked_songs_ids': liked_songs_ids
    })

@login_required
def upload_song(request):
    temp_path = None 
    
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # 1. CAPTURAR TIEMPOS y ARCHIVO ORIGINAL
                start_sec = float(form.cleaned_data.get('start_time') or 0)
                end_sec = float(form.cleaned_data.get('end_time') or 30)
                uploaded_audio_file = request.FILES['audio_file']
                
                if (end_sec - start_sec) > 32: 
                    end_sec = start_sec + 30
                    
                # 2. GUARDADO TEMPORAL PARA CELERY
                filename_temp = f"temp_{uuid.uuid4().hex[:8]}_{uploaded_audio_file.name}"
                temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', filename_temp)
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)

                # --- SELF-HEAL: Ensure processing.mp3 exists in MEDIA ---
                processing_dest = os.path.join(settings.MEDIA_ROOT, 'tracks', 'processing.mp3')
                if not os.path.exists(processing_dest):
                    os.makedirs(os.path.dirname(processing_dest), exist_ok=True)
                    # Try to copy from static
                    import shutil
                    static_processing = os.path.join(settings.BASE_DIR, 'static', 'audio', 'processing.mp3')
                    if os.path.exists(static_processing):
                        shutil.copy(static_processing, processing_dest)
                    else:
                        # Fallback creation if even static is missing (should not happen properly deployed)
                        with open(processing_dest, 'wb') as f: f.write(b'\0' * 1024)

                with open(temp_path, 'wb+') as destination:
                    for chunk in uploaded_audio_file.chunks():
                        destination.write(chunk)
                
                # 3. CREAR OBJETO CANCIÓN (Estado "Procesando")
                song = form.save(commit=False)
                song.uploader = request.user
                song.audio_file = "tracks/processing.mp3" # Placeholder
                song.full_audio_file = "tracks/processing.mp3" # Placeholder
                song.save()
                
                # 4. LANZAR TAREA SEGUNDO PLANO
                from .tasks import process_audio_task
                process_audio_task.delay(song.id, temp_path, start_sec, end_sec)

                check_and_award_badges(request.user)
                messages.success(request, "¡Canción recibida! Se está procesando en segundo plano y aparecerá pronto.")
                
                return redirect('home')

            except Exception as e:
                print(f"Error inicial en upload_song: {e}")
                messages.error(request, f"Ocurrió un error al subir el archivo: {e}")
                
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
                
        else:
            messages.error(request, "Por favor, revisa los errores del formulario antes de publicar.")
        
    else:
        form = SongForm()
    
    return render(request, 'upload.html', {'form': form})

@login_required
def rate_song(request, song_id, score):
    if 1 <= score <= 5:
        song = get_object_or_404(Song, id=song_id)
        Rating.objects.update_or_create(
            user=request.user,
            song=song,
            defaults={'score': score}
        )
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id, uploader=request.user)
    song.delete() # Esto activará signals.py para borrar archivos
    return redirect('profile')

@login_required
def toggle_favorite(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, song=song)
    
    if not created:
        favorite.delete()
        liked = False
    else:
        favorite.save()
        liked = True
        check_and_award_badges(request.user)
        
    return JsonResponse({'liked': liked})


def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    
    # Manejar el envío de comentarios
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.song = song
            comment.user = request.user
            comment.save()
            return redirect('song_detail', song_id=song.id)
    else:
        form = CommentForm()

    # Obtener comentarios existentes
    comments = song.comments.all().order_by('-created_at')
    
    # Verificar si le di like (para pintar el corazón en esta página también)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = request.user.favorites.filter(song=song).exists()

    return render(request, 'song_detail.html', {
        'song': song,
        'comments': comments,
        'form': form,
        'is_liked': is_liked
    })

@login_required
def delete_song(request, song_id):
    # 1. Buscamos la canción sin restricciones de usuario primero
    song = get_object_or_404(Song, id=song_id)
    
    # 2. VERIFICACIÓN DE SEGURIDAD 
    # Solo permitimos borrar si es el dueño O si es el Superusuario (Tú)
    if request.user == song.uploader or request.user.is_superuser:
        song.delete()
        # Si eres admin, te devolvemos al panel de ese usuario. Si no, a tu perfil.
        if request.user.is_superuser and request.user != song.uploader:
             return redirect('admin_user_detail', user_id=song.uploader.id)
        return redirect('profile')
    else:
        # Si un hacker intenta borrar algo ajeno, lo mandamos al Home
        return redirect('home')
    
def search(request):
    query = request.GET.get('q')
    songs = []
    users = []
    
    if query:
        # 1. Buscar Canciones (por Título O por Artista O por Género)
        songs = Song.objects.filter(
            Q(title__icontains=query) | 
            Q(artist__icontains=query) |
            Q(genre__name__icontains=query),
            is_private=False # Solo canciones públicas
        ).order_by('-created_at')

        # 2. Buscar Usuarios (por Username)
        users = User.objects.filter(
            username__icontains=query
        ).exclude(id=request.user.id) # No buscarme a mí mismo

    return render(request, 'search_results.html', {
        'query': query,
        'songs': songs,
        'users': users
    })

@login_required
def edit_song(request, song_id):
    # 1 Buscar
    song = get_object_or_404(Song, id=song_id)

    # 2. Seguridad: Solo el dueño (o un admin) puede editar
    if request.user != song.uploader and not request.user.is_superuser:
        return redirect('home')

    # 3. Procesar el formulario
    if request.method == 'POST':
        form = SongEditForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            # Volvemos al perfil después de guardar
            return redirect('profile')
    else:
        # Cargar los datos actuales en el formulario
        form = SongEditForm(instance=song)

    return render(request, 'edit_song.html', {'form': form, 'song': song})

# --- PLAYLISTS ---
from .models import Playlist
from .forms import PlaylistForm

@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            messages.success(request, "Playlist creada con éxito")
            return redirect('profile')
    else:
        form = PlaylistForm()
    
    return render(request, 'create_playlist.html', {'form': form})

@login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    # Seguridad: Si es privada y NO SOY el dueño, bloqueo
    if not playlist.is_public and request.user != playlist.owner:
        return redirect('home')
        
    return render(request, 'playlist_detail.html', {'playlist': playlist})

@login_required
def add_to_playlist(request, song_id, playlist_id):
    song = get_object_or_404(Song, id=song_id)
    playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
    
    playlist.songs.add(song)
    messages.success(request, f"Añadida a: {playlist.name}")
    return redirect(request.META.get('HTTP_REFERER', 'home'))
