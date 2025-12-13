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

    # DEBUG LOGS
    print(f"--- ANITA DEBUG ---")
    print(f"User: {request.user.username}")
    print(f"Liked Songs Count: {len(liked_songs)}")
    print(f"Public Songs Total: {Song.objects.filter(is_private=False).count()}")
    print(f"VIP Track Found (First Try): {vip_track}")

    # FALLBACK: Si ya escuchaste todo (o no hay nada nuevo), te muestra cualquier cancion publica
    if not vip_track:
        print("Triggering Fallback Logic...")
        vip_track = Song.objects.filter(is_private=False).order_by('?').first()
        print(f"VIP Track (Fallback): {vip_track}")

    # 4. Notificaciones No Leidas (Global)
    # Contar mensajes donde soy participante, NO soy el sender, y is_read=False
    from chat.models import Message
    total_unread_messages = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()

    print(f"User {request.user.username} has {total_unread_messages} unread messages.")

    return {
        'anita_bpm': current_bpm if current_bpm > 0 else "---",
        'anita_energy': round(current_energy * 100) if current_energy else 0,
        'anita_mood': (mood if current_energy > 0 else "Escaneando...") + " (v2.5)",
        'anita_track': vip_track,
        'total_unread_messages': total_unread_messages,
    }