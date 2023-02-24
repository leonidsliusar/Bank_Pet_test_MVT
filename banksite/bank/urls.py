from django.urls import path

from bank.services import *
from bank.views import *



urlpatterns = [
    path('bank/auth/', bank_auth, name='auth'),
    path('bank/wallet/transaction/', transaction_view, name='transaction_view'),
    path('bank/wallet/transaction/do/', transaction),
    path('bank/wallet/', wallet_view, name='wallet_view'),
    path('bank/reg/', bank_reg),
    path('bank/wallet/new/', new_wallet_generator),
    path('bank/wallet/<wallet_id>/', detail_wallet, name='detail_wallet'),
    path('bank/wallet/<wallet_id>/delete/', delete_wallet),
]