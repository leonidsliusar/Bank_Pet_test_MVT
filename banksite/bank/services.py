from _decimal import Decimal
import rstr
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from django.shortcuts import redirect
from bank.models import Wallet


def create_wallet(user_id):
    new_wallet = Wallet(user_id=user_id, wallet_id=rstr.xeger(r'[A-Z]{3}[-]\d{3}[-]\d{4}'))
    try:
        new_wallet.save()
    except IntegrityError:
        create_wallet(user_id)


@transaction.atomic
def make_transaction(request, source, recipient, quantity):
    if not source or not recipient or not quantity:
        message = 'You have to fill all fields'
        messages.add_message(request, messages.SUCCESS, message)
        return message
    s = None
    try:
        s = Wallet.objects.select_for_update().get(wallet_id=source)
        r = Wallet.objects.select_for_update().get(wallet_id=recipient)
    except ObjectDoesNotExist:
        if s:
            message = f'Target {recipient} wallet doesn\'t exists'
        else:
            message = f'Source {source} wallet doesn\'t exists'
        messages.add_message(request, messages.ERROR, message)
        return message
    if s.balance - Decimal(quantity) < 0:
        message = 'Not enough money on source wallet'
        messages.add_message(request, messages.ERROR, message)
    elif source == recipient:
        message = f'Source {source} wallet equal to target {recipient} wallet'
        messages.add_message(request, messages.ERROR, message)
    elif Decimal(quantity) <= 0:
        message = f'Invalid amount {quantity}'
        messages.add_message(request, messages.ERROR, message)
    else:
        s.balance -= Decimal(quantity)
        s.save()
        r.balance += Decimal(quantity)
        r.save()
        message = 'Transaction successful'
        messages.add_message(request, messages.SUCCESS, message)
    return message
