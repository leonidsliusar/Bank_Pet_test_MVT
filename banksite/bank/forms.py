from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from bank.models import Account


class Autorization(forms.ModelForm):
    login = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['login', 'password']


class Registration(forms.ModelForm):
    username = forms.CharField(label='Username', )
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name', max_length=55)
    last_name = forms.CharField(label='Surname', max_length=55)
    middle_name = forms.CharField(label='Middle name', max_length=55, required=False)
    birth_date = forms.DateField(label='Birth date',
                                 widget=forms.widgets.SelectDateWidget(years=range(date.today().year, 1900, -1)))
    email = forms.EmailField(label='e-mail')
    phone = forms.CharField(label='phone', validators=[validators.RegexValidator(regex='^\+?1?\d{9,15}$')])
    avatar = forms.ImageField(label='photo', required=False)

    class Meta:
        model = User
        exclude = ['registation_date']
        fields = ['username', 'password', 'password2', 'email', 'phone']
