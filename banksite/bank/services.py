from _decimal import Decimal
import rstr
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import redirect
from bank.models import Wallet


@login_required(login_url='../../auth/')
def new_wallet_generator(request):
    new_wallet = Wallet(user_id=request.POST.get('id'), wallet_id=rstr.xeger(r'[A-Z]{3}[-]\d{3}[-]\d{4}'))
    try:
        new_wallet.save()
    except AttributeError or TypeError:
        new_wallet_generator()
    finally:
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
@transaction.atomic
def transaction(request):
    source = request.POST.get('source')
    recipient = request.POST.get('recipient')
    quantity = request.POST.get('quantity')
    s = Wallet.objects.select_for_update().get(wallet_id=source)
    try:
        r = Wallet.objects.select_for_update().get(wallet_id=recipient)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'Target wallet doesn\'t exists')
        return redirect('transaction_view')
    if s.balance - Decimal(quantity) < 0:
        messages.add_message(request, messages.ERROR, 'Not enough money on source wallet')
        return redirect('transaction_view')
    elif source == recipient:
        messages.add_message(request, messages.ERROR, 'Source wallet equal to target wallet')
        return redirect('transaction_view')
    elif Decimal(quantity) <= 0:
        messages.add_message(request, messages.ERROR, 'Invalid amount')
        return redirect('transaction_view')
    else:
        s.balance -= Decimal(quantity)
        s.save()
        r.balance += Decimal(quantity)
        r.save()
        messages.add_message(request, messages.SUCCESS, 'Transaction successful')
        return redirect('transaction_view')
