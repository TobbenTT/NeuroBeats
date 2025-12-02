from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'cover_image', 'audio_file']

        # Esto es para darle estilo CSS de Bootstrap a los inputs
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la canción'}),
            'artist': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Banda o Artista'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control'}),
        }