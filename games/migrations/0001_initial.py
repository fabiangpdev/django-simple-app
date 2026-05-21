from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Genero',
                'verbose_name_plural': 'Generos',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Plataforma',
                'verbose_name_plural': 'Plataformas',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titulo')),
                ('status', models.CharField(
                    choices=[
                        ('pendiente', 'Pendiente'),
                        ('jugando', 'Jugando'),
                        ('completado', 'Completado'),
                        ('abandonado', 'Abandonado'),
                    ],
                    default='pendiente',
                    max_length=20,
                    verbose_name='Estado',
                )),
                ('rating', models.IntegerField(
                    blank=True,
                    null=True,
                    validators=[
                        django.core.validators.MinValueValidator(1),
                        django.core.validators.MaxValueValidator(10),
                    ],
                    verbose_name='Puntuacion (1-10)',
                )),
                ('cover_url', models.URLField(
                    blank=True,
                    help_text='URL de la imagen de portada del juego',
                    verbose_name='URL de Portada',
                )),
                ('notes', models.TextField(blank=True, verbose_name='Notas')),
                ('added_date', models.DateField(auto_now_add=True, verbose_name='Fecha de adicion')),
                ('genre', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='games.genre',
                    verbose_name='Genero',
                )),
                ('platform', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='games.platform',
                    verbose_name='Plataforma',
                )),
            ],
            options={
                'verbose_name': 'Juego',
                'verbose_name_plural': 'Juegos',
                'ordering': ['-added_date', 'title'],
            },
        ),
    ]
