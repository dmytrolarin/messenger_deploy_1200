"""
ASGI config for Messenger project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat_app.routing import ws_urlpatterns
from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Messenger.settings')

# Створюємо змінну application (об'єкт додатку)
application = ProtocolTypeRouter({
    # При http-запиті викликається стандартна функція get_asgi_application(), яка перенаправить запит в urls.py
    "http": get_asgi_application(),
    # При ws-запиті викликається функція, яка відправить запит у routing.py
    "websocket": AuthMiddlewareStack(
        URLRouter(ws_urlpatterns)
    )
})
