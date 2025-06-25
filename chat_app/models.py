from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Отримуємо модель користувача, яка використовується в проекті
UserModel = get_user_model()

class ChatGroup(models.Model):
    '''
    Модель для групи чату, яка містить назву групи та учасників.
    '''
    name = models.CharField(max_length = 200)
    users = models.ManyToManyField(UserModel)
    is_personal_chat = models.BooleanField(default = False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("chat", kwargs = {"group_id": self.pk})
    

class ChatMessage(models.Model):
    '''
    Модель для повідомлення в групі чату, яка містить текст повідомлення,
    автора, групу чату та дату і час створення повідомлення.
    '''
    content = models.TextField()
    author = models.ForeignKey(UserModel, on_delete = models.SET_NULL, null = True)
    chat_group = models.ForeignKey(ChatGroup, on_delete = models.CASCADE)
    date_time = models.DateTimeField(auto_now_add = True)
    views = models.ManyToManyField(UserModel, related_name = "viewed_messages" )