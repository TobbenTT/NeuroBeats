from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

# 1. Géneros Musicales
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Género")

    def __str__(self):
        return self.name

# 2. La Canción
class Song(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título")
    artist = models.CharField(max_length=100, verbose_name="Artista")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='songs')

    # Archivos multimedia
    cover_image = models.ImageField(upload_to='covers/', default='covers/default.png', verbose_name='Portada')
    audio_file = models.FileField(upload_to='tracks/', verbose_name='Archivo de Audio (.mp3)')

    # Metadatos
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_songs')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # NUEVO CAMPO (Solo una vez)
    is_private = models.BooleanField(default=False, verbose_name="Privado")

    # NUEVOS CAMPOS DE IA
    bpm = models.IntegerField(null=True, blank=True, verbose_name="BPM (Velocidad)")
    energy = models.FloatField(null=True, blank=True, verbose_name="Nivel de Energía")
    
    def average_rating(self):
        ratings = self.ratings.all().aggregate(Avg('score'))['score__avg']
        return round(ratings, 1) if ratings else None

    def __str__(self):
        return f"{self.title} - {self.artist}"

# 3. Interacciones: Clasificar
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Puntuación (1-5)")

    class Meta:
        unique_together = ('user', 'song')

# 4. Interacciones: Favoritos
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorites_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')

# 5. Comentarios
class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Comentario")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.user.username} en {self.song.title}"