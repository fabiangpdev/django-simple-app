from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'GameVault Admin'
admin.site.site_title = 'GameVault'
admin.site.index_title = 'Panel de Administracion'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('games.urls', namespace='games')),
]
