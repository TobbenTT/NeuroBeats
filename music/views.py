from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings 
from .models import Song, Rating, Favorite
from .forms import SongForm
from pydub import AudioSegment
import os
import uuid
from brain.engine import get_recommended_songs
from users.utils import check_and_award_badges

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
            
            # --- LÓGICA DE RECORTE DE AUDIO MEJORADA ---
            uploaded_audio = request.FILES['audio_file']
            
            # 1. Obtenemos los datos y forzamos float (por si acaso)
            # Si falla, usamos 0 y 30 como seguridad
            try:
                start_sec = float(form.cleaned_data.get('start_time') or 0)
                end_sec = float(form.cleaned_data.get('end_time') or 30)
            except ValueError:
                start_sec = 0.0
                end_sec = 30.0

            # 2. DEBUG: Mira esto en tu terminal negra cuando subas la canción
            print(f"✂️ CORTANDO AUDIO: Inicio={start_sec}s | Fin={end_sec}s")

            # 3. Validación de seguridad (Máximo 30s)
            if (end_sec - start_sec) > 32: 
                end_sec = start_sec + 30

            # 4. Procesamiento con PyDub
            audio = AudioSegment.from_file(uploaded_audio)
            
            # 5. CONVERSIÓN A ENTEROS (CRÍTICO: Pydub odia los decimales)
            start_ms = int(start_sec * 1000)
            end_ms = int(end_sec * 1000)
            
            # 6. Cortar
            cut_audio = audio[start_ms:end_ms]
            
            # 7. Guardar con nombre único para evitar caché
            import uuid # Importar esto arriba si puedes, si no, usa el nombre simple
            filename = f"cut_{uuid.uuid4().hex[:8]}_{uploaded_audio.name}"
            
            # Ruta absoluta del sistema
            save_path = os.path.join(settings.MEDIA_ROOT, 'tracks', filename)
            
            # Asegurar directorio
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Exportar
            cut_audio.export(save_path, format="mp3")
            
            # 8. Asignar ruta relativa a la Base de Datos
            song.audio_file = f"tracks/{filename}"
            song.uploader = request.user
            song.save()
            check_and_award_badges(request.user)
            
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

        if not created:
            favorite.delete()
            liked = False
        else:
            favorite.save()  # Asegúrate de guardar
            liked = True
            
            # ¡LLAMAMOS AL JUEZ! 🏅
            check_and_award_badges(request.user)
        
    return JsonResponse({'liked': liked})
    


