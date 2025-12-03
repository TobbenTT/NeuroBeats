from django import forms
from .models import Song, Comment

class SongForm(forms.ModelForm):
    # Campos ocultos (el usuario no los ve, JS los llena)
    start_time = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    end_time = forms.FloatField(widget=forms.HiddenInput(), initial=30)

    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'cover_image', 'audio_file', 'is_private']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la canción'}),
            'artist': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Banda o Artista'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            # Agregamos un ID al input de archivo para encontrarlo fácil con JS
            'audio_file': forms.FileInput(attrs={'class': 'form-control', 'id': 'audio-input', 'accept': 'audio/*'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'width: 25px; height: 25px;'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary', 
                'rows': 3, 
                'placeholder': '¿Qué opinas de este temazo?'
            }),
        }