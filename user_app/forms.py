from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    '''
    Створюємо кастомний клас для створення користувача, який наслідує клас UserCreationForm заради валідації.
    За допомогою метода __init__  користуємося конструктором полів, та ініціалізуємо форму. Редагуємо вже існуючи поля та їх плейсхолдери.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Логін"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Пароль"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Підтвердіть пароль"})
        
    avatar = forms.ImageField(required = False, label = "Аватар")
    date_of_birth = forms.DateField(label = "Дата народження", widget = forms.DateInput(attrs = {"type": "date"}))

class CustomAuthenticationForm(AuthenticationForm):
    '''
    Також ініціалізуємо кастомну форму для авторизації та через конструктор редагуємо два нових поля.
    '''
    def __init__(self,request, *args, **kwargs):
        super().__init__(request,*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Логін'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})