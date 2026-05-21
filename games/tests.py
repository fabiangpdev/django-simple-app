from django.test import TestCase
from django.urls import reverse

from .models import Game, Platform, Genre
from .forms import GameForm


class PlatformModelTest(TestCase):
    def test_str(self):
        platform = Platform.objects.create(name='PC')
        self.assertEqual(str(platform), 'PC')


class GenreModelTest(TestCase):
    def test_str(self):
        genre = Genre.objects.create(name='RPG')
        self.assertEqual(str(genre), 'RPG')


class GameModelTest(TestCase):
    def setUp(self):
        self.platform = Platform.objects.create(name='PC')
        self.genre = Genre.objects.create(name='RPG')
        self.game = Game.objects.create(
            title='The Witcher 3',
            platform=self.platform,
            genre=self.genre,
            status='completado',
            rating=10,
            notes='Increible juego de rol.',
        )

    def test_str(self):
        self.assertEqual(str(self.game), 'The Witcher 3')

    def test_estado_por_defecto(self):
        game = Game.objects.create(title='Juego Nuevo')
        self.assertEqual(game.status, 'pendiente')

    def test_get_absolute_url(self):
        expected = f'/juego/{self.game.pk}/'
        self.assertEqual(self.game.get_absolute_url(), expected)

    def test_status_choices_contiene_todos(self):
        choices = dict(Game.STATUS_CHOICES)
        self.assertIn('pendiente', choices)
        self.assertIn('jugando', choices)
        self.assertIn('completado', choices)
        self.assertIn('abandonado', choices)

    def test_get_status_color(self):
        self.game.status = 'jugando'
        self.assertEqual(self.game.get_status_color(), 'primary')
        self.game.status = 'completado'
        self.assertEqual(self.game.get_status_color(), 'success')


class GameListViewTest(TestCase):
    def setUp(self):
        platform = Platform.objects.create(name='PC')
        Game.objects.create(title='Juego A', status='jugando', platform=platform)
        Game.objects.create(title='Juego B', status='completado', platform=platform)
        Game.objects.create(title='Juego C', status='pendiente', platform=platform)

    def test_status_code_200(self):
        response = self.client.get(reverse('games:game_list'))
        self.assertEqual(response.status_code, 200)

    def test_usa_template_correcto(self):
        response = self.client.get(reverse('games:game_list'))
        self.assertTemplateUsed(response, 'games/game_list.html')

    def test_muestra_todos_los_juegos(self):
        response = self.client.get(reverse('games:game_list'))
        self.assertEqual(len(response.context['games']), 3)

    def test_filtro_por_status(self):
        response = self.client.get(reverse('games:game_list') + '?status=jugando')
        self.assertEqual(len(response.context['games']), 1)
        self.assertEqual(response.context['games'][0].title, 'Juego A')

    def test_stats_en_contexto(self):
        response = self.client.get(reverse('games:game_list'))
        self.assertIn('stats', response.context)
        self.assertEqual(response.context['stats']['total'], 3)

    def test_filtro_invalido_muestra_todos(self):
        response = self.client.get(reverse('games:game_list') + '?status=inexistente')
        self.assertEqual(len(response.context['games']), 3)


class GameDetailViewTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create(title='Test Game', status='jugando')

    def test_status_code_200(self):
        response = self.client.get(reverse('games:game_detail', kwargs={'pk': self.game.pk}))
        self.assertEqual(response.status_code, 200)

    def test_404_juego_inexistente(self):
        response = self.client.get(reverse('games:game_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_contexto_contiene_juego(self):
        response = self.client.get(reverse('games:game_detail', kwargs={'pk': self.game.pk}))
        self.assertEqual(response.context['game'].title, 'Test Game')


class GameCreateViewTest(TestCase):
    def test_get_devuelve_200(self):
        response = self.client.get(reverse('games:game_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_form.html')

    def test_post_valido_crea_juego(self):
        data = {'title': 'Nuevo Juego', 'status': 'pendiente', 'rating': '', 'cover_url': '', 'notes': ''}
        response = self.client.post(reverse('games:game_create'), data)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_post_invalido_no_crea(self):
        data = {'title': '', 'status': 'pendiente'}
        response = self.client.post(reverse('games:game_create'), data)
        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(response.status_code, 200)


class GameUpdateViewTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create(title='Juego Original', status='pendiente')

    def test_get_devuelve_200(self):
        response = self.client.get(reverse('games:game_update', kwargs={'pk': self.game.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_actualiza_juego(self):
        data = {'title': 'Juego Actualizado', 'status': 'completado', 'rating': 9, 'cover_url': '', 'notes': ''}
        self.client.post(reverse('games:game_update', kwargs={'pk': self.game.pk}), data)
        self.game.refresh_from_db()
        self.assertEqual(self.game.title, 'Juego Actualizado')
        self.assertEqual(self.game.status, 'completado')


class GameDeleteViewTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create(title='Juego a Eliminar', status='pendiente')

    def test_get_devuelve_200(self):
        response = self.client.get(reverse('games:game_delete', kwargs={'pk': self.game.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_elimina_juego(self):
        response = self.client.post(reverse('games:game_delete', kwargs={'pk': self.game.pk}))
        self.assertEqual(Game.objects.count(), 0)
        self.assertRedirects(response, reverse('games:game_list'))


class GameFormTest(TestCase):
    def test_formulario_valido(self):
        data = {'title': 'Juego Valido', 'status': 'pendiente'}
        form = GameForm(data=data)
        self.assertTrue(form.is_valid())

    def test_titulo_requerido(self):
        data = {'title': '', 'status': 'pendiente'}
        form = GameForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_rating_fuera_de_rango(self):
        data = {'title': 'Test', 'status': 'pendiente', 'rating': 15}
        form = GameForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_rating_valido(self):
        data = {'title': 'Test', 'status': 'jugando', 'rating': 8}
        form = GameForm(data=data)
        self.assertTrue(form.is_valid())

class StatsViewTest(TestCase):
    def test_status_code_200(self):
        response = self.client.get(reverse('games:stats'))
        self.assertEqual(response.status_code, 200)

    def test_usa_template_correcto(self):
        response = self.client.get(reverse('games:stats'))
        self.assertTemplateUsed(response, 'games/stats.html')

    def test_contexto_con_datos(self):
        Game.objects.create(title='Juego X', status='completado', rating=8)
        response = self.client.get(reverse('games:stats'))
        self.assertEqual(response.context['total'], 1)
        self.assertIsNotNone(response.context['avg_rating'])
