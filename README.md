# GameVault - Inventario Personal de Videojuegos

Aplicacion Django para gestionar tu coleccion personal de videojuegos.
Desarrollada como proyecto de la asignatura con Docker.

## Tematicas implementadas

| Tema | Donde |
|------|-------|
| Modelos | `games/models.py` — Game, Platform, Genre |
| Vistas de funcion | `games/views.py` — `stats_view` |
| Vistas genericas | `games/views.py` — ListView, DetailView, CreateView, UpdateView, DeleteView |
| URLConf | `games/urls.py` y `config/urls.py` |
| Formularios | `games/forms.py` — GameForm con widgets Bootstrap |
| CRUD SQLite | Crear/Leer/Actualizar/Eliminar juegos |
| Panel Admin | `games/admin.py` — con filtros, busqueda y edicion en lista |
| Testing | `games/tests.py` — 25+ tests de modelos, vistas y formularios |

---

## Ejecutar con Docker

### Requisitos
- Docker Desktop instalado

### Pasos

```bash
# 1. Construir e iniciar
docker-compose up --build

# 2. Abrir en el navegador
http://localhost:8000

# Panel admin
http://localhost:8000/admin
# Usuario: admin  |  Contrasena: admin123
```

### Detener
```bash
docker-compose down
```

---

## Ejecutar los tests

```bash
docker-compose exec web python manage.py test games -v 2
```

---

## Despliegue en la web

### Opcion 1: Render (recomendado para SQLite)

1. Subir el codigo a GitHub
2. Crear cuenta en render.com
3. New > Web Service > conectar repo
4. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn config.wsgi:application`
5. En "Disks", agregar un disco en `/opt/render/project/src` para persistir la BD
6. Variables de entorno:
   ```
   SECRET_KEY=<clave-secreta-aleatoria>
   DEBUG=False
   ALLOWED_HOSTS=<tu-dominio>.onrender.com
   CSRF_TRUSTED_ORIGINS=https://<tu-dominio>.onrender.com
   ```

### Opcion 2: Railway

1. Subir a GitHub
2. railway.app > New Project > Deploy from GitHub
3. Agregar las mismas variables de entorno
4. Railway detecta el Dockerfile automaticamente

---

## Estructura del proyecto

```
projectdjango/
├── config/             # Configuracion Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── games/              # App principal
│   ├── models.py       # Game, Platform, Genre
│   ├── views.py        # Vistas genericas + funcion
│   ├── forms.py        # GameForm
│   ├── admin.py        # Panel admin
│   ├── urls.py         # URLConf de la app
│   ├── tests.py        # Tests
│   ├── fixtures/       # Datos iniciales
│   └── templates/      # HTML con Bootstrap 5
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
