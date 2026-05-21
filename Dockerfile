FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py createsuperuser --noinput 2>/dev/null || true && python manage.py loaddata games/fixtures/initial_data.json 2>/dev/null || true && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
