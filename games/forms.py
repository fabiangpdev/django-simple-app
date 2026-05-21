from django import forms
from .models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'platform', 'genre', 'status', 'rating', 'cover_url', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: The Witcher 3, Elden Ring...',
            }),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': '1 - 10',
            }),
            'cover_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://ejemplo.com/portada.jpg',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tus notas sobre el juego...',
            }),
        }
        labels = {
            'title': 'Titulo del Juego',
            'platform': 'Plataforma',
            'genre': 'Genero',
            'status': 'Estado',
            'rating': 'Puntuacion (1-10)',
            'cover_url': 'URL de Portada',
            'notes': 'Notas personales',
        }
