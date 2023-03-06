from datetime import date

from django import forms
from django.contrib.auth.models import User
from django.core import validators
from phone_field import PhoneField

from bank.models import Account


class Autorization(forms.ModelForm):
    login = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ['login', 'password']
class Registration(forms.ModelForm):
    username = forms.CharField(label='Логин',)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя', max_length=55)
    last_name = forms.CharField(label='Фамилия', max_length=55)
    middle_name = forms.CharField(label='Отчество', max_length=55, required=False)
    birth_date = forms.DateField(label='Дата рождения', widget=forms.widgets.SelectDateWidget(years=range(date.today().year, 1900, -1)))
    email = forms.EmailField(label='Электронная почта')
    phone = forms.CharField(label='Телефон', validators=[validators.RegexValidator(regex='^\+?1?\d{9,15}$')])
    avatar = forms.ImageField(label='Фото', required=False)
    class Meta:
        model = User
        exclude = ['registation_date']
        fields =['username', 'password', 'password2', 'email', 'phone']

