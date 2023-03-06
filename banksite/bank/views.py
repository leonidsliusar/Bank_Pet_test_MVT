from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME, authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from bank.forms import Autorization, Registration
from bank.models import *
from bank.serializer import query_serializer, query_serializer
import logging
from django.contrib import messages
logger = logging.getLogger('main')

"""request.method == 'POST':
    username = request.POST.get('login')
    password = request.POST.get('password')
    find = User.objects.filter(username=username, password=password).values('username', 'password')
    data = {'username': username, 'password': password}
    user = User.objects.get(username=username)
    if data in find:"""

def bank_auth(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        #logger.debug(f'Успешная авторизация {username}')
        return redirect(reverse('wallet_view'))
    else:
        messages.debug(request, 'Пользователя с таким логином и паролем нет')
        auth_form = Autorization
        return render(request, 'home.html', {'form': auth_form})


def logout_view(request):
    logout(request)
    return redirect('auth')

def bank_reg(request):
    reg_form = Registration(request.POST)
    if request.method == 'POST' and request.POST.get('password')==request.POST.get('password2') and reg_form.is_valid():
        user = User()
        account = Account()
        user.username = request.POST.get('username')
        user.set_password(request.POST.get('password'))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        account.middle_name = request.POST.get('middle_name')
        account.birth_date = request.POST.get('birth_date_year') + "-" + request.POST.get('birth_date_month') + "-" + request.POST.get('birth_date_day')
        account.avatar = request.POST.get('avatar')
        account.phone = request.POST.get('phone')
        user.save()
        account.user_id = user.id
        account.save()
        return redirect('../auth')
    else:
        reg_form = Registration
        return render(request, 'reg.html', {'form': reg_form})

@login_required(login_url='../auth/')
def wallet_view(request):
    try:
        username = request.user
        user_data = User.objects.filter(username=username).values('id', 'username', 'first_name', 'last_name', 'email')
        wallet_data = User.objects.get(username=username).wallet_set.all().values('wallet_id', 'balance')
        context = {**user_data[0], **{'wallets': wallet_data}}
        #serialize_wallet = query_serializer(wallet_data)
        serialize_wallet = query_serializer(data=wallet_data)
        request.session['data'] = {**user_data[0], **serialize_wallet}
        return render(request, 'account.html', context)
    except:
        return redirect('../auth')



@login_required(login_url='../auth/')
def detail_wallet(request, wallet_id):
    id = request.user.id
    wallet_data = User.objects.get(id=id).wallet_set.filter(wallet_id=wallet_id).values('wallet_id', 'balance')
    context = wallet_data[0]
    return render(request, 'wallet.html', context)

@login_required(login_url='../../auth/')
def transaction_view(request):
    username = request.user
    wallet_data = User.objects.get(username=username).wallet_set.all().values('wallet_id', 'balance')
    context = query_serializer(wallet_data)
    return render(request, 'transaction.html', context)