from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.GameListView.as_view(), name='game_list'),
    path('juego/nuevo/', views.GameCreateView.as_view(), name='game_create'),
    path('juego/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('juego/<int:pk>/editar/', views.GameUpdateView.as_view(), name='game_update'),
    path('juego/<int:pk>/eliminar/', views.GameDeleteView.as_view(), name='game_delete'),
    path('estadisticas/', views.stats_view, name='stats'),
]
