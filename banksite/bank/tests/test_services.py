import pytest
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from bank.models import Wallet
from bank.services import create_wallet


@pytest.mark.django_db(transaction=True)
def test_create_wallet(create_test_user):
    user_id = User.objects.get(pk=1).id
    create_wallet(user_id)
    result = Wallet.objects.filter(user_id=user_id).exists()
    assert result == True


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('source_id, target_id, amount, source_start_bal', [
    (1, 2, 10, 100),
    (1, 2, 100, 10),
    (1, 2, -10, 100)
]
                         )
def test_make_transaction(create_test_user, auth_and_login_user, add_wallet,
                          source_id, target_id, amount, source_start_bal):
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
    endpoint = reverse('do_transaction')
    response = client.post(endpoint, data)
    storage = messages.get_messages(response.wsgi_request)
    message = [str(message) for message in storage][0]
    source_balance = Wallet.objects.get(wallet_id=source_id).balance
    target_balance = Wallet.objects.get(wallet_id=target_id).balance
    if amount > source_start_bal or amount <= 0:
        assert source_balance == source_start_bal and target_balance == 0
        if amount > source_start_bal:
            expected_message = f'Not enough money on source wallet'
        else:
            expected_message = f'Invalid amount {amount}'
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
    endpoint = reverse('do_transaction')
    data.update(recipient=source_id)
    response = client.post(endpoint, data)
    storage = messages.get_messages(response.wsgi_request)
    message = [str(message) for message in storage][0]
    source_balance = Wallet.objects.get(wallet_id=source_id).balance
    target_balance = Wallet.objects.get(wallet_id=target_id).balance
    assert source_balance == source_start_bal and target_balance == 0
    assert message == f'Source {source_id} wallet equal to target {source_id} wallet'


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
    endpoint = reverse('do_transaction')
    data.update(recipient=source_id+target_id)
    response = client.post(endpoint, data)
    storage = messages.get_messages(response.wsgi_request)
    message = [str(message) for message in storage][0]
    source_balance = Wallet.objects.get(wallet_id=source_id).balance
    assert source_balance == source_start_bal
    assert message == f'Target {source_id+target_id} wallet doesn\'t exists'
