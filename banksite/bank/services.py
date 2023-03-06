"""from RegexGenerator import RegexGenerator
myRegexGenerator = RegexGenerator("ABF-555-7676")
print(myRegexGenerator.get_regex())"""
import time
from _decimal import Decimal
import rstr
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect
from bank.models import *


def get_object(model, attribute):
    return model.objects.get(wallet_id=attribute)

@login_required(login_url='../../auth/')
def new_wallet_generator(request):
    new_wallet = Wallet(user_id=request.POST.get('id'), wallet_id=rstr.xeger(r'[A-Z]{3}[-]\d{3}[-]\d{4}'))
    try:
        new_wallet.save()
    except:
        new_wallet_generator()
    finally:
        return redirect('wallet_view')

@login_required(login_url='../../auth/')
def delete_wallet(request, wallet_id):
    wallet = get_object(Wallet, request.POST.get('id'))
    wallet.delete()
    return redirect('wallet_view')

@login_required(login_url='../../auth/')
@transaction.atomic
def transaction(request):
    source = request.POST.get('source')
    recipient = request.POST.get('recipient')
    quantity = request.POST.get('quantity')
    s = Wallet.objects.select_for_update().get(wallet_id=source)
    try:
        r = Wallet.objects.select_for_update().get(wallet_id=recipient)
    except:
        messages.add_message(request, messages.ERROR, 'Указаный кошелек получателя не существует')
        return redirect('transaction_view')
    if s.balance - Decimal(quantity)< 0:
        messages.add_message(request, messages.ERROR, 'Недостаточно денег на счете')
        return redirect('transaction_view')
    elif source == recipient:
        messages.add_message(request, messages.ERROR, 'Счет получателя совпадает со счетом отправителя')
        return redirect('transaction_view')
    elif Decimal(quantity) <= 0:
        messages.add_message(request, messages.ERROR, 'Указана некорректная сумма перевода')
        return redirect('transaction_view')
    else:
        s.balance -= Decimal(quantity)
        s.save()
        r.balance += Decimal(quantity)
        r.save()
        messages.add_message(request, messages.SUCCESS, 'Перевод совершен')
        return redirect('transaction_view')
