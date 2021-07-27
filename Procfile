web: daphne justchat.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=justchat.settings -v2