from music.models import Song
from django.db.models import Avg

def dj_anita_status(request):
    """
    Este código se ejecuta en CADA página y le da datos a DJ Anita.

    """
    if not request.user.is_authenticated:
        return{}
    
    # 1 Analizar el VIBE del usuario
    liked_songs = request.user.favorites.values_list('song_id', flat=True)
    stats = Song.objects.filter(id__in=liked_songs).aggregate(
        avg_bpm=Avg('bpm'),
        avg_energy=Avg('energy')
    )

    current_bpm = int(stats['avg_bpm'] or 0)
    current_energy = stats['avg_energy'] or 0

    # 2. Determinar el "Mood" (Estado de ánimo)
    mood = "Neutral"
    if current_energy > 0.7: mood = "Eufórico"
    elif current_energy < 0.4: mood = "Chill"
    elif current_bpm > 130: mood = "Acelerado"

    # 3. La recomendación VIP de Anita (Solo una)
    # Busca algo que NO hayas escuchado y que coincida con tu Vibe
    vip_track = Song.objects.filter(is_private=False).exclude(id__in=liked_songs).order_by('?').first()

    return {
        'anita_bpm': current_bpm,
        'anita_energy': round(current_energy * 100), # Porcentaje
        'anita_mood': mood,
        'anita_track': vip_track
    }