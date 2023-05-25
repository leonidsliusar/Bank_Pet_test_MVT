from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from bank.forms import Autorization, Registration
from bank.models import *
import logging
from django.contrib import messages
from bank.services import create_wallet, make_transaction

logger = logging.getLogger('main')


def bank_auth(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('wallet_view'))
    else:
        messages.debug(request, 'User doesn\'t exists')
        auth_form = Autorization
        return render(request, 'home.html', {'form': auth_form})


def logout_view(request):
    logout(request)
    return redirect('auth')


def bank_reg(request):
    reg_form = Registration(request.POST)
    if request.method == 'POST' and request.POST.get('password') == request.POST.get(
            'password2') and reg_form.is_valid():
        user = User()
        account = Account()
        user.username = request.POST.get('username')
        user.set_password(request.POST.get('password'))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        account.middle_name = request.POST.get('middle_name')
        account.birth_date = request.POST.get('birth_date_year') + "-" + request.POST.get(
            'birth_date_month') + "-" + request.POST.get('birth_date_day')
        account.avatar = request.POST.get('avatar')
        account.phone = request.POST.get('phone')
        user.save()
        account.user_id = user.id
        account.save()
        return redirect(reverse(bank_auth))
    else:
        reg_form = Registration
        return render(request, 'reg.html', {'form': reg_form})


@login_required(login_url='../auth/')
def wallet_view(request):
    try:
        user_id = request.user.id
        first_name = request.user.first_name
        wallets = Wallet.objects.filter(user_id=user_id).all()
        data = {
            'first_name': first_name,
            'id': user_id,
            'wallets': wallets
        }
        return render(request, 'account.html', context=data)
    except AttributeError or ValueError or TypeError:
        return redirect(reverse(bank_auth))


@login_required(login_url='../auth/')
def detail_wallet(request, wallet_id):
    user_id = request.user.id
    try:
        wallet_data = get_object_or_404(Wallet, user=user_id, wallet_id=wallet_id)
        context = {'balance': wallet_data.balance, 'wallet_id': wallet_data.wallet_id}
        return render(request, 'wallet.html', context)
    except Http404:
        messages.error(request, f'You ain\'t got wallet {wallet_id}')
        return redirect(reverse(wallet_view))


@login_required(login_url='../../auth/')
def transaction_view(request):
    user_id = request.user.id
    wallet_data = Wallet.objects.filter(user=user_id).values('wallet_id', 'balance')
    context = {'wallet_data': wallet_data}
    return render(request, 'transaction.html', context)


@login_required(login_url='../../auth/')
def new_wallet_generator(request):
    user_id = request.POST.get('id')
    create_wallet(user_id)
    return redirect('wallet_view')


@login_required(login_url='../../auth/')
def delete_wallet(request, wallet_id):
    wallet = Wallet.objects.get(wallet_id=wallet_id)
    if wallet.balance != 0:
        messages.add_message(request, messages.ERROR, 'The wallet isn\'t empty')
        return redirect('detail_wallet', wallet_id=wallet_id)
    wallet.delete()
    return redirect('wallet_view')


@login_required(login_url='../../auth/')
def transaction(request):
    source = request.POST.get('source')
    recipient = request.POST.get('recipient')
    quantity = request.POST.get('quantity')
    message = make_transaction(request, source, recipient, quantity)
    return redirect('transaction_view')