from celery import shared_task
from django.conf import settings
from .models import Song
from .analysis import analyze_audio
from pydub import AudioSegment
import os
import uuid
from users.utils import check_and_award_badges

@shared_task
def process_audio_task(song_id, temp_file_path, start_sec, end_sec):
    """
    Tarea asíncrona para procesar el audio (recortar + crear versión HQ).
    Se ejecuta en segundo plano vía Celery.
    """
    try:
        # Re-obtener la canción de la DB
        song = Song.objects.get(id=song_id)
        
        # Cargar audio con Pydub (puede ser muy pesado, por eso usamos Celery)
        audio = AudioSegment.from_file(temp_file_path)
        
        original_filename = os.path.basename(temp_file_path)

        # Helper para asegurar extensión .mp3
        base_name = os.path.splitext(original_filename)[0]
        
        # A) Versión 1: Clip (30s) OPTIMIZADO para preview (128 kbps)
        cut_audio = audio[int(start_sec * 1000) : int(end_sec * 1000)]
        clip_filename = f"clip_{uuid.uuid4().hex[:8]}_{base_name}.mp3" # FORCE .mp3
        clip_save_path = os.path.join(settings.MEDIA_ROOT, 'tracks', clip_filename)
        os.makedirs(os.path.dirname(clip_save_path), exist_ok=True)
        
        # Exportar clip a 128 kbps
        cut_audio.export(clip_save_path, format="mp3", parameters=["-b:a", "128k"]) 
        
        # B) Versión 2: Pista Completa (HQ) para streaming (320 kbps)
        hq_filename = f"hq_{uuid.uuid4().hex[:8]}_{base_name}.mp3" # FORCE .mp3
        hq_save_path = os.path.join(settings.MEDIA_ROOT, 'tracks', 'full_hq', hq_filename)
        os.makedirs(os.path.dirname(hq_save_path), exist_ok=True)
        
        # Exportar pista completa a 320 kbps
        audio.export(hq_save_path, format="mp3", parameters=["-b:a", "320k"])
        
        # Actualizar Modelo
        song.audio_file = f"tracks/{clip_filename}"
        song.full_audio_file = f"tracks/full_hq/{hq_filename}"
        
        # Analizar Audio (IA)
        bpm, energy = analyze_audio(clip_save_path)
        if bpm:
            song.bpm = bpm
            song.energy = energy
            
        song.save()
        
        # Limpieza
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        # Dar insignias (si aplica)
        check_and_award_badges(song.uploader)
        
        return f"Successfully processed song {song_id}"

    except Exception as e:
        import traceback
        import shutil
        
        # --- DIAGNOIS: REPORTAR POR QUÉ FALLÓ ---
        # Esto ayudará a ver si ffmpeg realmente es visible o no
        ffmpeg_path = shutil.which("ffmpeg")
        env_path = os.environ.get('PATH')
        
        print(f"CRITICAL ERROR processing song {song_id}: {e}")
        print(f"DIAGNOSTIC - FFmpeg path found: {ffmpeg_path}")
        print(f"DIAGNOSTIC - System PATH: {env_path}")
        
        traceback.print_exc()

        # Limpiar archivo temporal si falló
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        return f"Error: {e}"
