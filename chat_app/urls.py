from django.urls import path
from .views import *


urlpatterns = [
    path("chat/<int:group_id>", ChatView.as_view(), name="chat"),
    path("", ChatGroupListView.as_view(), name = "groups"),
    path("personal-chats/", PersonalChatListView.as_view(), name = "personal_chats"),
    path("create-personal-chat/<int:user_id>", create_personal_chat, name = "create_personal_chat")
]