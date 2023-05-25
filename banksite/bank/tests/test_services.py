import asyncio

from asgiref.sync import sync_to_async
from django.test import AsyncClient
import aiohttp
import pytest
from django.contrib import messages
from django.urls import reverse
from bank.models import Wallet
from bank.services import new_wallet_generator, delete_wallet, transaction


@pytest.mark.django_db(transaction=True)
def test_new_waller_generator(create_test_user, auth_and_login_user):
    client = create_test_user
    wrapper_fixt = auth_and_login_user
    user_data = wrapper_fixt(client)
    user_id = user_data['id']
    endpoint = reverse(new_wallet_generator)
    response = client.post(endpoint, {'id': user_id})
    assert response.status_code == 302
    assert response.url == reverse('wallet_view')
    assert Wallet.objects.all().exists() == True
    assert Wallet.objects.first().user_id == user_id


@pytest.mark.django_db(transaction=True)
def test_delete_wallet(create_test_user, auth_and_login_user, add_wallet, wallet_id=1):
    client = create_test_user
    wrapper_fixt = auth_and_login_user
    user_data = wrapper_fixt(client)
    wrapper_fixt_wall = add_wallet
    wrapper_fixt_wall(user_data, wallet_id)
    assert Wallet.objects.all().exists() == True
    endpoint = reverse(delete_wallet, args=[wallet_id])
    response = client.post(endpoint)
    assert response.status_code == 302
    assert response.url == reverse('wallet_view')
    assert Wallet.objects.all().exists() == False


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('source_id, target_id, amount, source_start_bal', [
    (1, 2, 10, 100),
    (1, 2, 100, 10),
    (1, 2, -10, 100)
]
                         )
def test_transaction(create_test_user, auth_and_login_user, add_wallet, source_id, target_id, amount, source_start_bal):
    data = {
        'source': source_id,
        'recipient': target_id,
        'quantity': amount
    }
    client = create_test_user
    wrapper_fixt = auth_and_login_user
    user_data = wrapper_fixt(client)
    wrapper_fixt_wall = add_wallet
    wrapper_fixt_wall(user_data, source_id)
    wrapper_fixt_wall(user_data, target_id)
    Wallet.objects.filter(wallet_id=source_id).update(balance=source_start_bal)
    endpoint = reverse(transaction)
    response = client.post(endpoint, data)
    assert response.status_code == 302
    assert response.url == reverse(('transaction_view'))
    source_balance = Wallet.objects.get(wallet_id=source_id).balance
    target_balance = Wallet.objects.get(wallet_id=target_id).balance
    storage = messages.get_messages(response.wsgi_request)
    message = [str(message) for message in storage][0]
    if amount > source_start_bal or amount <= 0:
        assert source_balance == source_start_bal and target_balance == 0
        if amount > source_start_bal:
            expected_message = 'Not enough money on source wallet'
        else:
            expected_message = 'Invalid amount'
    else:
        assert source_balance == source_start_bal - amount and target_balance == amount
        expected_message = 'Transaction successful'
    assert message == expected_message


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('source_id, target_id, amount, source_start_bal', [
    (1, 2, 10, 100),
]
                         )
def test_transaction_target_equal_source(create_test_user, auth_and_login_user, add_wallet, source_id,
                                         target_id, amount, source_start_bal):
    data = {
        'source': source_id,
        'recipient': target_id,
        'quantity': amount
    }
    client = create_test_user
    wrapper_fixt = auth_and_login_user
    user_data = wrapper_fixt(client)
    wrapper_fixt_wall = add_wallet
    wrapper_fixt_wall(user_data, source_id)
    wrapper_fixt_wall(user_data, target_id)
    Wallet.objects.filter(wallet_id=source_id).update(balance=source_start_bal)
    endpoint = reverse(transaction)
    source_balance = Wallet.objects.get(wallet_id=source_id).balance
    target_balance = Wallet.objects.get(wallet_id=target_id).balance
    data['recipient'] = source_id
    response = client.post(endpoint, data)
    storage = messages.get_messages(response.wsgi_request)
    message = [str(message) for message in storage][0]
    assert response.status_code == 302
    assert response.content.decode() == ''
    assert response.url == reverse('transaction_view')
    assert source_balance == source_start_bal and target_balance == 0
    assert message == 'Source wallet equal to target wallet'


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('source_id, target_id, amount, source_start_bal', [
    (1, 2, 10, 100),
]
                         )
def test_transaction_wallet_doesnt_exists(create_test_user, auth_and_login_user, add_wallet, source_id,
                                          target_id, amount, source_start_bal):
    data = {
        'source': source_id,
        'recipient': target_id,
        'quantity': amount
    }
    client = create_test_user
    wrapper_fixt = auth_and_login_user
    user_data = wrapper_fixt(client)
    wrapper_fixt_wall = add_wallet
    wrapper_fixt_wall(user_data, source_id)
    Wallet.objects.filter(wallet_id=source_id).update(balance=source_start_bal)
    endpoint = reverse(transaction)
    source_balance = Wallet.objects.get(wallet_id=source_id).balance
    response = client.post(endpoint, data)
    storage = messages.get_messages(response.wsgi_request)
    message = [str(message) for message in storage][0]
    assert response.status_code == 302
    assert response.url == reverse(('transaction_view'))
    assert source_balance == source_start_bal
    assert message == 'Target wallet doesn\'t exists'
