import asyncio

import aiohttp
import pytest
from django.contrib.auth import authenticate
from django.test import Client, AsyncClient
from django.contrib.auth.models import User

from bank.models import Wallet


@pytest.fixture
def create_test_user():
    data = {
        'id': 1,
        'username': 'test',
        'password': 'testtest',
        'first_name': 'test_name',
        'last_name': 'test_surname',
        'email': 'test@test.com',
    }
    client = Client()
    User.objects.create_user(**data)
    return client


@pytest.fixture
def auth_and_login_user():
    def wrapper(client):
        data = {
            'id': 1,
            'username': 'test',
            'password': 'testtest',
            'first_name': 'test_name',
            'last_name': 'test_surname',
            'email': 'test@test.com',
        }
        user = authenticate(username=data['username'], password=data['password'])
        client.force_login(user)
        return data

    return wrapper


@pytest.fixture
def add_wallet():
    def wrapper(data, wallet_id=1):
        wallet = Wallet.objects.create(user_id=data['id'], wallet_id=wallet_id)
        wallet.save()
        wallet_data = {'balance': format(wallet.balance, '.2f'), 'wallet_id': wallet.wallet_id}
        return wallet_data

    return wrapper


