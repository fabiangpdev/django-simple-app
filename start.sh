#!/bin/sh
python manage.py migrate
python manage.py createsuperuser --noinput 2>/dev/null || true
python manage.py loaddata games/fixtures/initial_data.json 2>/dev/null || true
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
