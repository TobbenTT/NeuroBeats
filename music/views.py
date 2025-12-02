from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse  # <--- VITAL para los likes
from .models import Song, Rating, Favorite  # <--- VITAL para guardar likes
from .forms import SongForm
from pydub import AudioSegment
from brain.engine import get_recommended_songs
import os

def home(request):
    # 1. OBTIENE LAS RECOMENDACIONES (IA)
    recommended_songs = get_recommended_songs(request.user)
    
    # 2. OBTIENE EL RESTO (Exploración Global)
    # Sacamos los IDs de las recomendadas para no repetirlas abajo
    recommended_ids = [song.id for song in recommended_songs]
    
    # Traemos todas las canciones que NO están en la lista de recomendados
    explore_songs = Song.objects.exclude(id__in=recommended_ids).order_by('-created_at')
    
    # 3. LIKES (Para pintar los corazones)
    liked_songs_ids = []
    if request.user.is_authenticated:
        liked_songs_ids = request.user.favorites.values_list('song_id', flat=True)
    
    return render(request, 'home.html', {
        'recommended_songs': recommended_songs, # Lista 1 (Centro)
        'explore_songs': explore_songs,         # Lista 2 (Abajo)
        'liked_songs_ids': liked_songs_ids
    })
@login_required
def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            
            # --- LÓGICA DE RECORTE CON ONDAS ---
            uploaded_audio = request.FILES['audio_file']
            
            # Obtenemos los datos exactos del formulario visual
            start_sec = form.cleaned_data.get('start_time', 0)
            end_sec = form.cleaned_data.get('end_time', 30)
            
            # Validacion de seguridad: Que no dure más de 30s
            if (end_sec - start_sec) > 32: # Damos 2s de margen por lag
                end_sec = start_sec + 30

            # Procesamiento con PyDub
            audio = AudioSegment.from_file(uploaded_audio)
            
            # Convertir segundos a milisegundos
            start_ms = start_sec * 1000
            end_ms = end_sec * 1000
            
            # Cortar
            cut_audio = audio[start_ms:end_ms]
            
            # Guardar
            filename = f"cut_{uploaded_audio.name}" # Cambiamos nombre para evitar caché
            save_path = f"media/tracks/{filename}"
            
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            cut_audio.export(save_path, format="mp3")
            
            song.audio_file = f"tracks/{filename}"
            song.uploader = request.user
            song.save()
            return redirect('home')
    else:
        form = SongForm()
    
    return render(request, 'upload.html', {'form': form})

@login_required
def rate_song(request, song_id, score):
    # Solo aceptamos votos del 1 al 5
    if 1 <= score <= 5:
        song = get_object_or_404(Song, id=song_id)
        
        # update_or_create: Magia de Django.
        # Si ya votaste, actualiza tu voto (Edit). Si no, crea uno nuevo.
        Rating.objects.update_or_create(
            user=request.user,
            song=song,
            defaults={'score': score}
        )
    
    # Nos devuelve a la página donde estábamos (el perfil)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def delete_song(request, song_id):
    # Buscamos la canción, PERO asegurándonos de que el uploader sea el usuario actual.
    # Si alguien intenta borrar una canción ajena cambiando la URL, le dará Error 404.
    song = get_object_or_404(Song, id=song_id, uploader=request.user)
    
    # Borramos la canción (y sus archivos de audio/imagen asociados gracias a Django)
    song.delete()
    
    # Volvemos al perfil
    return redirect('profile')

@login_required
def toggle_favorite(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    
    # Intenta buscar el like. Si existe lo borra, si no existe lo crea.
    favorite, created = Favorite.objects.get_or_create(user=request.user, song=song)
    
    if not created:
        # Si NO se creó recién, significa que YA existía -> Lo borramos (Unlike)
        favorite.delete()
        liked = False
    else:
        # Si se creó recién -> (Like)
        liked = True
    
    # Respondemos solo con datos, no con HTML
    return JsonResponse({'liked': liked})