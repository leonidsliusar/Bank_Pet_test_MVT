"""from RegexGenerator import RegexGenerator
myRegexGenerator = RegexGenerator("ABF-555-7676")
print(myRegexGenerator.get_regex())"""
import rstr
from django.shortcuts import redirect

from bank.models import *


def new_wallet_generator(request):
    new_wallet = Wallet(account_id=request.POST.get('id'), wallet_id=rstr.xeger(r'[A-Z]{3}[-]\d{3}[-]\d{4}'))
    try:
        new_wallet.save()
    except:
        new_wallet_generator()
    finally:
        return redirect('wallet_view')


def delete_wallet(request, wallet_id):
    wallet = Wallet.objects.get(wallet_id=request.POST.get('id'))
    wallet.delete()
    return redirect('wallet_view')

def transaction(request):
    pass