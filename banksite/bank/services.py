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
    s = Wallet.objects.select_for_update().get(wallet_id=source)
    try:
        r = Wallet.objects.select_for_update().get(wallet_id=recipient)
    except ObjectDoesNotExist:
        message = messages.add_message(request, messages.ERROR, 'Target wallet doesn\'t exists')
        return message
    if s.balance - Decimal(quantity) < 0:
        message = messages.add_message(request, messages.ERROR, 'Not enough money on source wallet')
    elif source == recipient:
        message = messages.add_message(request, messages.ERROR, 'Source wallet equal to target wallet')
    elif Decimal(quantity) <= 0:
        message = messages.add_message(request, messages.ERROR, 'Invalid amount')
    else:
        s.balance -= Decimal(quantity)
        s.save()
        r.balance += Decimal(quantity)
        r.save()
        message = messages.add_message(request, messages.SUCCESS, 'Transaction successful')
    return message
