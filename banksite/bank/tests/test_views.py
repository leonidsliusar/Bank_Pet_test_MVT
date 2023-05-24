import pytest
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.test import Client
from django.urls import reverse


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
