from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
# Create your models here.

# 1 Generos Musicales
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Genero")

    def __str__(self):
        return self.name

# 2 La cancion
class Song(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titulo")
    artist = models.CharField(max_length=100, verbose_name="Artista")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='songs')

    # Archivos multimedia
    cover_image = models.ImageField(upload_to='covers/', default='covers/default.png', verbose_name='Portada')
    audio_file = models.FileField(upload_to='tracks/', verbose_name='Archivo de Audio (.mp3)')

    # Metadatos
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_songs')
    created_at = models.DateTimeField(auto_now_add=True)

    # PEGA ESTO AL FINAL DE LA CLASE SONG (respetando la indentación)
    def average_rating(self):
        ratings = self.ratings.all().aggregate(Avg('score'))['score__avg']
        return round(ratings, 1) if ratings else None

    def __str__(self):
        return f"{self.title} - {self.artist}"
    
# 3 Interacciones: Clasificar para la IA
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Puntacion (1-5)")

    class Meta:
        unique_together = ('user', 'song')

# 4 Interacciones: Favoritos
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorites_by')
    added_at =models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')