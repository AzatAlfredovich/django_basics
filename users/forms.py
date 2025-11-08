from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=30,
        required=True,
        help_text="Поле обязательно к заполнению. Введите почту.",
    )
    avatar = forms.ImageField(
        required=False,
        help_text="Поле необязательно к заполнению. Загрузите изображение.",
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text="Поле необязательно к заполнению. Введите номер телефона.",
    )
    country = forms.CharField(
        max_length=30,
        required=False,
        help_text="Поле необязательно к заполнению. Введите страну проживания.",
    )
    usable_password = None

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "phone_number",
            "country",
            "avatar",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с такой почтой уже зарегистрирован!")
        else:
            return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError(
                "Номер телефона должен состоять только из цифр!"
            )
        return phone_number
