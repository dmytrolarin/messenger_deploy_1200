from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, change_avatar

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name = "login"),
    path("logout/", CustomLogoutView.as_view(), name = "logout"),
    path("change_avatar/", change_avatar, name = "change_avatar")
]