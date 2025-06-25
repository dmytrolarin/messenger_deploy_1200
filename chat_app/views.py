from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .forms import MessageForm
from .models import ChatGroup, ChatMessage
from django.shortcuts import redirect
from django.db.models import Q

class ChatView(FormView):
    # Вказуємо шаблон для відображення
    template_name = "chat_app/chat.html"
    # Вказуємо форму з якою буде працювати клас
    form_class = MessageForm

    def dispatch(self, request, *args, **kwargs):
        '''
            Цей метод спрацьовує перед відображенням сторінки. У ньому прописується логіка, що повинна спрацьовувати перед відображенням сторінки.
        '''

        # Отримуємо параметр з динамічної URL-адреси
        chat_group_id = self.kwargs['group_id']
        # Шукаємо чат по його pk
        chat = ChatGroup.objects.get(pk = chat_group_id)
        # Отримуємо авторизованого користувача
        user = request.user
        # Якщо користувач є у чаті
        if user in chat.users.all():
            # Отримуємо усі повідомлення, що знаходсятья у поточній чат-групі
            current_group_messages = ChatMessage.objects.filter(chat_group = chat)
            # Перебираємо усі повідомлення з поточної групи
            for message in current_group_messages:
                # Додаємо поточного користувача по зв'язку ManyToMany, як того, хто переглянув повідомлення
                message.views.add(user)
                # Зберігаємо зміни у об'єкті повідомлення
                message.save()

            # Повертаємо звичайний виклик методу
            return super().dispatch(request, *args, **kwargs)
        else:
            # Якщо користувача немає - повертаємо на сторінку груп
            return redirect('groups')
       
    def get_context_data(self, **kwargs):
        '''
            Цей метод потрібен для обробки контексту, що буде переданий до шаблонізатору.
        '''
        # Отримуємо контекст
        data = super().get_context_data(**kwargs)
        # Отримуємо параметр з динамічної URL-адреси
        chat_group_id = self.kwargs["group_id"]
        # Отримуємо усі повідомлення цього чату
        messages = ChatMessage.objects.filter(chat_group_id = chat_group_id)
        # Додаємо повідомлення до контексту
        data["messages"] = messages
        # Передаємо чат у контекст
        data["chat_group"] = ChatGroup.objects.get(pk = chat_group_id)
        # Повертаємо змінений контекст
        return data

    
class ChatGroupListView(ListView):
    '''
        Створюємо класс для відображння спику груп.
    '''

    # Вказуємо модель, з якої будуть братися об'єкти
    model = ChatGroup
    # Вказуємо шаблон для відображення
    template_name = "chat_app/groups.html"
    # Вказуємо ім'я, за яким буде називатися наш список у шаблонізаторі
    context_object_name = "list_groups"

class PersonalChatListView(ListView):
    '''
    Створюємо клас для відображення списку особистих чатів
    '''

    template_name = "chat_app/personal_chats.html" 
    context_object_name = "list_chats"

    def get_queryset(self):
        '''
        Визначаємо набір данних, який буде використовуватись для відображення
        '''
        #Створюємо список користувачів без поточного
        queryset = get_user_model().objects.exclude(pk=self.request.user.pk)
        return queryset

def create_personal_chat(request, user_id):
    '''
        Функція відображення, що відповідає за отримання персонального чату (або створення, якщо його не існує)
    '''

    # Отримуємо авторизованого на данний момент користувача
    current_user = request.user
    # Отримуємо користувача, з яким маємо отримати персональний чат
    user_to_connect = get_user_model().objects.get(pk=user_id)
    # Фільтруємо персональний чат групу двох користувачів
    group = ChatGroup.objects.filter(is_personal_chat=True).filter(users = current_user).filter(users = user_to_connect).first()
    # Перевіряємо, якщо не існує між цими користувачами персональна група
    if not group:
        # Ствоюємо персональну групу в разі її відсутності
        group = ChatGroup.objects.create(
            name = f"Чат між {current_user} та {user_to_connect}",
            is_personal_chat = True
        )
        # Додаємо двох користувачів до нової групи
        group.users.add(current_user, user_to_connect)
        # Зберігаємо нову персональну чат групу
        group.save()
    # Перенаправляємо користувача по url персональної чат групи
    return redirect(group.get_absolute_url())