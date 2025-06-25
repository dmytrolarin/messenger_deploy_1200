'''
Файл для маршрутизації WebSocket запитів (аналог urls.py)
'''
from django.urls import path
from .consumers import ChatConsumer

# Створюємо список з url для обробки WebSocket-запитів
ws_urlpatterns = [
    # Створємо шлях для chat, вказуючи ChatConsumer як асинхронний обробник для WebSocket запиту
    path("chat/<int:group_id>", ChatConsumer.as_asgi()) 
]