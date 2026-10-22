from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model  # <-- самый надёжный способ
from django.forms import BooleanField
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs.setdefault('class', 'form-check-input')
            else:
                field.widget.attrs.setdefault('class', 'form-control')


class CustomUserCreationForm(StyleMixin, UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text='(Необязательно, но полезно для связи)',
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
            'type': 'tel',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        required=True,
        help_text='Обязательно для регистрации'
    )  # делаем email обязательным

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Переименовываем стандартные поля
        self.fields['username'].label = "Придумайте логин"
        self.fields['email'].label = "Ваш Email"

        # 2. САМОЕ ВАЖНОЕ: меняем названия для паролей
        # password1 — это первое поле пароля
        self.fields['password1'].label = "Придумайте пароль"
        # password2 — это подтверждение пароля
        self.fields['password2'].label = "Повторите пароль"

        # Опционально: меняем help_text (подсказки под полем)
        self.fields['username'].help_text = "(Необязательно)"
        self.fields['password1'].help_text = "Минимум 8 символов."
        self.fields['password2'].help_text = "Введите тот же пароль ещё раз."

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        if not phone:
            return phone  # если поле необязательное и пусто — просто возвращаем

        # Удаляем всё, кроме цифр и плюса в начале
        cleaned = ''.join(c for c in phone if c.isdigit() or (c == '+' and phone.index(c) == 0))

        # Если после очистки остался только плюс или пусто — ошибка
        digits = ''.join(c for c in cleaned if c.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError('Номер телефона слишком короткий. Укажите минимум 10 цифр.')

        return cleaned


class CustomUserLoginForm(StyleMixin, AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label="Запомнить меня")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Логин или email'
        self.fields['password'].label = 'Пароль'

        self.fields['username'].widget.attrs.update({'placeholder': 'Логин или email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})
