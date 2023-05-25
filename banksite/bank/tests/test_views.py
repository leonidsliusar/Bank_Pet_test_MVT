import pytest
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.test import Client
from django.urls import reverse

from bank import services, views
from bank.models import Wallet
from bank.views import delete_wallet, new_wallet_generator, transaction


@pytest.mark.django_db
@pytest.mark.parametrize('login, password', [('test', 'test_pass')])
def test_bank_auth(monkeypatch, login, password):
    client = Client()
    User.objects.create_user(login, 'test@test.com', password)
    endpoint = reverse('auth')
    response = client.post(endpoint, data={'login': login, 'password': password})
    assert response.status_code == 302
    assert response.url == reverse('wallet_view')
    response = client.post(endpoint, data={'login': login + password, 'password': login + password})
    assert response.status_code == 200


@pytest.mark.django_db
def test_bank_reg():
    data = {
        'username': 'test',
        'password': 'testtest',
        'password2': 'testtest',
        'first_name': 'test_name',
        'last_name': 'test_surname',
        'middle_name': '',
        'email': 'test@test.com',
        'birth_date_year': 2000,
        'birth_date_month': 1,
        'birth_date_day': 1,
        'phone': '+90000000000'
    }
    client = Client()
    endpoint = reverse('reg')
    response = client.post(endpoint, data=data)
    assert response.status_code == 302
    assert response.url == reverse('auth')
    data = {}
    response = client.post(endpoint, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_wallet_view(create_test_user, auth_and_login_user):
    client = create_test_user
    fixt_wrapper = auth_and_login_user
    data = fixt_wrapper(client)
    response = client.get(reverse('wallet_view'))
    csrf_token = response.context['csrf_token']
    assert response.status_code == 200
    expected_result = render_to_string('account.html', context={'csrf_token': csrf_token, **data})
    result = response.content.decode()
    assert result == expected_result


@pytest.mark.django_db
def test_detail_wallet(create_test_user, auth_and_login_user, add_wallet):
    client = create_test_user
    fixt_wrapper = auth_and_login_user
    data = fixt_wrapper(client)
    fixt_wall_wrapper = add_wallet
    wallet_data = fixt_wall_wrapper(data)
    response = client.get(reverse('detail_wallet', args=[wallet_data['wallet_id']]))
    csrf_token = response.context['csrf_token']
    assert response.status_code == 200
    expected_result = render_to_string('wallet.html', context={'csrf_token': csrf_token, **wallet_data})
    result = response.content.decode()
    assert result == expected_result
    response = client.get(reverse('detail_wallet', args=[100]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_transaction_view(create_test_user, auth_and_login_user, add_wallet):
    client = create_test_user
    fixt_wrapper = auth_and_login_user
    data = fixt_wrapper(client)
    fixt_wall_wrapper = add_wallet
    wallet_data = fixt_wall_wrapper(data)
    wallets = [{'balance': wallet_data['balance'], 'wallet_id': wallet_data['wallet_id']}]
    response = client.get(reverse('transaction_view'))
    csrf_token = response.context['csrf_token']
    assert response.status_code == 200
    expected_result = render_to_string(
        'transaction.html', context={'csrf_token': csrf_token, 'wallet_data': wallets, 'user_id': data['id']})
    result = response.content.decode()
    assert result == expected_result


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


def stub_create_wallet(user_id=None):
    pass


@pytest.mark.django_db(transaction=True)
def test_new_wallet_generator(monkeypatch, create_test_user, auth_and_login_user):
    monkeypatch.setattr(views, 'create_wallet', stub_create_wallet)
    client = create_test_user
    wrapper_fixt = auth_and_login_user
    wrapper_fixt(client)
    response = client.post(reverse(new_wallet_generator))
    assert response.status_code == 302


def stub_make_transaction(request, source, recipient, quantity):
    pass


@pytest.mark.django_db(transaction=True)
def test_transaction(monkeypatch, create_test_user, auth_and_login_user):
    monkeypatch.setattr(views, 'make_transaction', stub_make_transaction)
    client = create_test_user
    wrapper_fixt = auth_and_login_user
    wrapper_fixt(client)
    response = client.post(reverse(transaction))
    assert response.status_code == 302
