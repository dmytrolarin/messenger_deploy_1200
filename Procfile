release: python manage.py migrate
web: uvicorn Messenger.asgi:application --host 0.0.0.0 --port $PORT