from .models import Badge
from music.models import Song, Rating, Favorite
from django.db.models import Count

def check_and_award_badges(user):
    """
    Analiza el historial del usuario y le da insignias si cumple los requisitos.
    """
    profile = user.profile
    
    # 1. INSIGNIA: "Melómano" (Escuchar/Dar like a 5 canciones de cualquier tipo)
    total_likes = user.favorites.count()
    if total_likes >= 5:
        award_badge(profile, "Melómano", "fas fa-headphones", "Amante de la música (5+ Likes)")

    # 2. INSIGNIA: "Rockstar" (Gustarle 3 canciones de Rock)
    rock_likes = user.favorites.filter(song__genre__name__iexact="Rock").count()
    if rock_likes >= 3:
        award_badge(profile, "Rockstar", "fas fa-guitar", "Alma de Rock (3+ Likes en Rock)")

    # 3. INSIGNIA: "Pop Star" (Gustarle 3 canciones de Pop)
    pop_likes = user.favorites.filter(song__genre__name__iexact="Pop").count()
    if pop_likes >= 3:
        award_badge(profile, "Pop Star", "fas fa-microphone-alt", "Fan del Pop (3+ Likes en Pop)")

    # 4. INSIGNIA: "Productor" (Subir 1 canción)
    uploaded_songs = user.uploaded_songs.count()
    if uploaded_songs >= 1:
        award_badge(profile, "Productor", "fas fa-upload", "Creador de contenido (1+ Subida)")

def award_badge(profile, name, icon, description):
    # Buscamos o creamos la insignia en la BD
    badge, created = Badge.objects.get_or_create(
        name=name,
        defaults={'icon_name': icon, 'description': description, 'criteria': name.lower()}
    )
    
    # Si el usuario NO la tiene, se la damos
    if badge not in profile.badges.all():
        profile.badges.add(badge)
        print(f"🏅 ¡Insignia otorgada a {profile.user.username}: {name}!")