release: python manage.py migrate
web: gunicorn platyplus.wsgi:application --preload --workers 1
