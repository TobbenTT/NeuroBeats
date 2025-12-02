from django.contrib import admin
from .models import Song, Genre, Rating

# Register your models here.

#Lista de canciones

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'genre', 'uploader', 'created_at')
    search_fields = ('title', 'artist')
    list_filter = ('genre',)

admin.site.register(Genre)
admin.site.register(Rating)