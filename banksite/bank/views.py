from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView

from banksite.bank.models import Account


def home(request):
    return HttpResponse("Hey")

"""class AccountView(DetailView):
    model = Account"""