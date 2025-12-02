from music.models import Song
from collections import Counter

def get_recommended_songs(user):
    # 1. SI EL USUARIO NO ESTÁ LOGUEADO
    if not user.is_authenticated:
        return Song.objects.all().order_by('-created_at')[:8]

    # 2. OBTENER GUSTOS (Usando el nombre correcto 'favorites_by')
    favorite_genres = Song.objects.filter(
        favorites_by__user=user
    ).values_list('genre__id', flat=True)

    # Fallback a Ratings si no hay Favoritos
    if not favorite_genres:
        favorite_genres = Song.objects.filter(
            ratings__user=user,
            ratings__score__gte=3
        ).values_list('genre__id', flat=True)

    # 3. COLD START (Si no sabemos nada, mostramos todo)
    if not favorite_genres:
        return Song.objects.all().order_by('-created_at')[:8]

    # 4. ALGORITMO PRINCIPAL
    genre_counts = Counter(favorite_genres)
    most_common_genre_id = genre_counts.most_common(1)[0][0]
    
    # Buscamos canciones de ese género...
    recommendations = Song.objects.filter(genre_id=most_common_genre_id)
    
    # ... que NO haya escuchado aún (likes)
    liked_songs_ids = user.favorites.values_list('song_id', flat=True)
    recommendations = recommendations.exclude(id__in=liked_songs_ids)
    
    # --- CORRECCIÓN: EL PLAN B (Fallback) ---
    # Si después de filtrar no queda nada (porque ya escuchó todo de ese género)
    if not recommendations.exists():
        # Devolvemos canciones nuevas de CUALQUIER género
        return Song.objects.exclude(id__in=liked_songs_ids).order_by('-created_at')[:8]
    
    return recommendations.order_by('-created_at')[:8]