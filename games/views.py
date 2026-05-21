from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Count, Avg
from django.contrib import messages

from .models import Game, Platform, Genre
from .forms import GameForm


class GameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'

    def get_queryset(self):
        queryset = Game.objects.select_related('platform', 'genre').all()
        status = self.request.GET.get('status')
        if status in dict(Game.STATUS_CHOICES):
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        context['stats'] = {
            'total': Game.objects.count(),
            'jugando': Game.objects.filter(status='jugando').count(),
            'completado': Game.objects.filter(status='completado').count(),
            'pendiente': Game.objects.filter(status='pendiente').count(),
            'abandonado': Game.objects.filter(status='abandonado').count(),
        }
        return context


class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'


class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'games/game_form.html'

    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.title}" fue agregado a tu coleccion.')
        return super().form_valid(form)


class GameUpdateView(UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'games/game_form.html'

    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.title}" fue actualizado correctamente.')
        return super().form_valid(form)


class GameDeleteView(DeleteView):
    model = Game
    template_name = 'games/game_confirm_delete.html'
    success_url = reverse_lazy('games:game_list')

    def form_valid(self, form):
        messages.success(self.request, f'"{self.object.title}" fue eliminado de tu coleccion.')
        return super().form_valid(form)


def stats_view(request):
    total = Game.objects.count()

    status_data = []
    color_map = {
        'pendiente': 'secondary',
        'jugando': 'primary',
        'completado': 'success',
        'abandonado': 'danger',
    }
    for code, label in Game.STATUS_CHOICES:
        count = Game.objects.filter(status=code).count()
        pct = round(count * 100 / total) if total > 0 else 0
        status_data.append({
            'code': code,
            'label': label,
            'count': count,
            'pct': pct,
            'color': color_map[code],
        })

    avg_rating = Game.objects.filter(
        rating__isnull=False
    ).aggregate(avg=Avg('rating'))['avg']

    top_platforms = Platform.objects.annotate(
        num_games=Count('game')
    ).filter(num_games__gt=0).order_by('-num_games')[:5]

    context = {
        'total': total,
        'status_data': status_data,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
        'top_platforms': top_platforms,
    }
    return render(request, 'games/stats.html', context)
