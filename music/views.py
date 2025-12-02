from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Song, Rating
from .forms import SongForm
from pydub import AudioSegment
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