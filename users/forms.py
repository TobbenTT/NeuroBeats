from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'is_private']
        
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'width: 20px; height: 20px;'}),
        }