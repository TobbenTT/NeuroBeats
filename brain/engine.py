from music.models import Song, Rating, Favorite
from django.db.models import Count, Avg, Q
import random

def get_recommended_songs(user):
    """
    IA Nivel 2: Recomendación Híbrida (Gustos + Energía + BPM)
    """
    # 1. Si no hay usuario o es nuevo, mostramos lo más popular/reciente
    if not user.is_authenticated:
        return Song.objects.filter(is_private=False).order_by('-created_at')[:8]

    # 2. Obtener lo que le gusta al usuario (Likes y Ratings altos)
    liked_songs_ids = user.favorites.values_list('song_id', flat=True)
    
    # 3. ANÁLISIS DE PERFIL SÓNICO 🎛️
    # Calculamos el promedio de BPM y Energía de las canciones que le gustan
    user_stats = Song.objects.filter(id__in=liked_songs_ids).aggregate(
        avg_bpm=Avg('bpm'),
        avg_energy=Avg('energy')
    )
    
    target_bpm = user_stats['avg_bpm']
    target_energy = user_stats['avg_energy']

    # 4. BUSCAR CANCIONES SIMILARES (El Algoritmo)
    # Buscamos canciones que:
    # A) No sean privadas
    # B) No las haya escuchado aún (excluir liked_ids)
    # A) No sean privadas
    # B) No las haya escuchado aún (excluir liked_ids)
    recommendations = Song.objects.filter(is_private=False).exclude(id__in=liked_songs_ids)

    if target_bpm and target_energy:
        # Si tenemos datos, aplicamos la MATEMÁTICA:
        # Buscamos canciones que estén en un rango cercano (+- 20 BPM y +- 0.2 Energía)
        print(f"🧠 CEREBRO: Buscando música estilo -> BPM: {int(target_bpm)} | Energía: {round(target_energy, 2)}")
        
        # Intentamos filtrar. Si nos quedamos sin canciones, el if de abajo nos salvará.
        filtered_recommendations = recommendations.filter(
            bpm__range=(target_bpm - 20, target_bpm + 20),
            energy__range=(target_energy - 0.2, target_energy + 0.2)
        )
        # Solo aplicamos el filtro si devuelve ALGO. Si no, usamos la base (recommendations) sin filtro estricto.
        if filtered_recommendations.exists():
            recommendations = filtered_recommendations

    # --- LÓGICA DE SALVACIÓN (FALLBACKS) ---
    
    # 1. Si tenemos recomendaciones validas (ya sean filtradas o solo "no escuchadas")
    if recommendations.exists():
        return recommendations.order_by('?')[:8]

    # 2. Si NO hay recomendaciones (ej: escuchó todo lo que existe), devolvemos CUALQUIER COSA pública
    # "Redescubrimiento"
    return Song.objects.filter(is_private=False).order_by('?')[:8]