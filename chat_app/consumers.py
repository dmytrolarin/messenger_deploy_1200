'''
consumers.py - файл, який обробляє логіку веб-сокет запитів, аналог views.py
'''
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .forms import MessageForm
from channels.db import database_sync_to_async
from .models import ChatMessage
import time


class ChatConsumer(AsyncWebsocketConsumer):
    '''
        Створюємо клас ChatConsumer, який відповідає за з'єднання сервера з клієнтом. Він відловлює та обробляє ws запити 
    '''

    async def connect(self):
        '''
            Метод connect відпрацьовує, коли користувач надсилає запит про підключення
        '''
        # Отримуємо id групи з динамічної URL під іменем "group_id"
        self.group_id = str(self.scope['url_route']['kwargs']['group_id'])
        # Під'єднуємо поточного користувача (тобто його канал) до групи, котра вказана в динамічному URL
        await self.channel_layer.group_add(
            self.group_id, 
            self.channel_name
        )
        # Запит про підключення схвалений
        await self.accept()

    async def receive(self, text_data):
        '''
            Метод receive спрацьовує, коли сервер отримує повідомленя від клієнта
        '''
        # Зберігаеємо повідомлення у базу даних та у змінну "saved_message"
        saved_message = await self.save_message(text_data)
        # Відправляємо повідомлення всім участникам групи
        await self.channel_layer.group_send(
            # Вказуємо назву групи
            self.group_id, 
            {
                # Вказуємо тип обробника (метод, що викличиться для відправки повідомлення)
                "type": "send_message_to_chat",
                # Передаємо повідомлення користувача через event, send_message_to_chat
                "text_data": text_data,
                # Передаємо ім'я автора повідомлення
                "username": self.scope["user"].username,
                # Передаємо час, коли було відправлено повідомлення
                "datetime": saved_message.date_time.isoformat(), 
            }
        )
        
    async def send_message_to_chat(self, event):
        '''
            Метод, який надсилає повідомлення усім участникам групи 
        '''

        # Перетворюємо текст з формату json у python словник
        dict_data = json.loads(event["text_data"])
        # Передаємо дані у форму для валідації
        form = MessageForm(dict_data)
        # У випадку якщо всі поля валідні
        if form.is_valid():
            # Надсилаємо повідомленя назад через WebSocket клієнту
            text_to_send = f"{event['username']}: {dict_data['message']}"
            # Перетворюємо python словник у json рядок
            text_data = json.dumps({"message": text_to_send, "datetime": event["datetime"]}, ensure_ascii = False)
            # Відправляємо повідомлення користувачу
            await self.send(text_data = text_data)
        else:
            # Виводимо помилку, якщо форма не валідна
            print("Error, form isnt valid!")

    @database_sync_to_async
    def save_message(self, message_data):
        '''
            Опрацьовуємо та зберігаємо повідомлення у базу даних.
            Повертає об'єкт повідомлення для подальшого використання.
        '''
        # Отримуємо користувача, котрий під'єднався к цьому WebSocket (автора повідомлення)
        user = self.scope['user']
        # Перетворюємо текст повідомлення з формату json у python словник
        message_data = json.loads(message_data)
        # Створюємо та одразу зберігаємо повідомлення з даними, котрі передали у цю фукцнію
        message = ChatMessage.objects.create(
            content = message_data['message'],
            author = user,
            chat_group_id = self.group_id,
            date_time = time.time()
        )
        # Повертаємо створений об'єкт повідомлення
        return message