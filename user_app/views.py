from django.views.generic.edit import CreateView 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Profile
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.http import JsonResponse


class RegisterView(CreateView):
    '''
        Створюємо клас відображення сторінки реєстрації, успадковуючи CreateView, для того щоб при заповнені форми створювався об'єкт моделі.
    '''
    # Вказуємо форму, що буде створювати об'єкт
    form_class = CustomUserCreationForm
    # Вказуємо шаблон для відображення
    template_name = 'user_app/register.html'
    # Вказуємо шлях для редіректу після успішного заповнення форми
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        data = form.cleaned_data
        birthday = data["date_of_birth"]
        avatar = data.get('avatar')
        user = self.object
        Profile.objects.create(user = user, avatar = avatar, date_of_birth = birthday)
        return response


class CustomLoginView(LoginView):
    '''
        Створюємо клас відображення сторінки логіну, успадковуючи LoginView, для того щоб при заповнені форми був авторизован користувач.
    '''
    # Вказуємо форму, що буде авторизовувати користувача
    form_class = CustomAuthenticationForm
    # Вказуємо шаблон для відображення
    template_name = 'user_app/login.html'


class CustomLogoutView(LogoutView):
    '''
        Створюємо клас відображення для виходу з акаунту.
    '''
    # Вказуємо на яку сторінку перейти після логауту
    next_page = 'login'


def change_avatar(request):
    avatar = request.FILES.get("avatar")
    profile = request.user.profile
    profile.avatar = avatar
    profile.save()

    return JsonResponse({})