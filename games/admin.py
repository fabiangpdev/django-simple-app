from django.contrib import admin
from .models import Game, Platform, Genre


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'platform', 'genre', 'status', 'rating', 'added_date']
    list_filter = ['status', 'platform', 'genre']
    search_fields = ['title', 'notes']
    list_editable = ['status', 'rating']
    readonly_fields = ['added_date']
    fieldsets = (
        ('Informacion General', {
            'fields': ('title', 'platform', 'genre', 'cover_url')
        }),
        ('Estado y Puntuacion', {
            'fields': ('status', 'rating')
        }),
        ('Notas', {
            'fields': ('notes',)
        }),
        ('Metadatos', {
            'fields': ('added_date',),
            'classes': ('collapse',)
        }),
    )
