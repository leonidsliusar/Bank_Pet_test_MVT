from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib import messages
import rstr

from bank.forms import Autorization, Registration
from bank.models import *


def bank_auth(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        find = Account.objects.filter(login=login, password=password).values('login', 'password')
        data = {'login': login, 'password': password}
        if data in find:
            request.session['context'] = data
            return redirect(reverse('wallet_view'))
        else:
            return HttpResponse('Пользователя с таким логином и паролем нет')
    else:
        auth_form = Autorization
        return render(request, 'home.html', {'form': auth_form})

def bank_reg(request):
    reg_form = Registration(request.POST)
    if request.method == 'POST' and request.POST.get('password')==request.POST.get('password2') and reg_form.is_valid():
        user = Account()
        user.login = request.POST.get('login')
        user.password = request.POST.get('password')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.middle_name = request.POST.get('middle_name')
        user.birth_date = request.POST.get('birth_date_year') + "-" + request.POST.get('birth_date_month') + "-" + request.POST.get('birth_date_day')
        user.email = request.POST.get('email')
        user.avatar = request.POST.get('avatar')
        user.phone = request.POST.get('phone')
        user.save()
        return redirect('bank/')
    else:
        reg_form = Registration
        return render(request, 'reg.html', {'form': reg_form})


def wallet_view(request):
    login = request.session['context']['login']
    user_data = Account.objects.filter(login=login).values()
    wallet_data = Account.objects.get(login=login).wallet_set.all().values('wallet_id', 'balance')
    context = {**user_data[0], **{'wallets': wallet_data}}
    print(context)
    return render(request, 'account.html', context)

def detail_wallet(request, wallet_id):
    wallet_data = Wallet.objects.filter(wallet_id=wallet_id).values('wallet_id', 'balance')
    context = wallet_data[0]
    return render(request, 'wallet.html', context)


