from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Platform(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Plataforma'
        verbose_name_plural = 'Plataformas'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'
        ordering = ['name']

    def __str__(self):
        return self.name


class Game(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('jugando', 'Jugando'),
        ('completado', 'Completado'),
        ('abandonado', 'Abandonado'),
    ]

    title = models.CharField(max_length=200, verbose_name='Titulo')
    platform = models.ForeignKey(
        Platform,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Plataforma',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Genero',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendiente',
        verbose_name='Estado',
    )
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Puntuacion (1-10)',
    )
    cover_url = models.URLField(
        blank=True,
        verbose_name='URL de Portada',
        help_text='URL de la imagen de portada del juego',
    )
    notes = models.TextField(blank=True, verbose_name='Notas')
    added_date = models.DateField(auto_now_add=True, verbose_name='Fecha de adicion')

    class Meta:
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'
        ordering = ['-added_date', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('games:game_detail', kwargs={'pk': self.pk})

    def get_status_color(self):
        colors = {
            'jugando': 'primary',
            'completado': 'success',
            'pendiente': 'secondary',
            'abandonado': 'danger',
        }
        return colors.get(self.status, 'secondary')
