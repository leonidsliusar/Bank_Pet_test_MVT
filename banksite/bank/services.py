"""from RegexGenerator import RegexGenerator
myRegexGenerator = RegexGenerator("ABF-555-7676")
print(myRegexGenerator.get_regex())"""
import time
from _decimal import Decimal
import rstr
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from bank.models import *





def get_object(model, attribute):
    return model.objects.get(wallet_id=attribute)

def new_wallet_generator(request):
    new_wallet = Wallet(account_id=request.POST.get('id'), wallet_id=rstr.xeger(r'[A-Z]{3}[-]\d{3}[-]\d{4}'))
    try:
        new_wallet.save()
    except:
        new_wallet_generator()
    finally:
        return redirect('wallet_view')


def delete_wallet(request, wallet_id):
    wallet = get_object(Wallet, request.POST.get('id'))
    wallet.delete()
    return redirect('wallet_view')

@transaction.atomic
def transaction(request):
    source = request.POST.get('source')
    recipient = request.POST.get('recipient')
    quantity = request.POST.get('quantity')
    s = Wallet.objects.select_for_update().get(wallet_id=source)
    r = Wallet.objects.select_for_update().get(wallet_id=recipient)
    if s.balance - Decimal(quantity)< 0:
        messages.success(request, 'Недостаточно денег на счете')
        return redirect('transaction_view')

    elif source == recipient:
        messages.success(request, 'Счет получателя совпадает со счетом отправителя')
        return redirect('transaction_view')
    elif Decimal(quantity) <= 0:
        messages.success(request, 'Указана некорректная сумма перевода')
        return redirect('transaction_view')
    else:
        s.balance -= Decimal(quantity)
        s.save()
        time.sleep(20)
        r.balance += Decimal(quantity)
        r.save()
        messages.success(request, 'Перевод совершен')
        return redirect('transaction_view')
