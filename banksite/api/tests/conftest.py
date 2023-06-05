import subprocess
import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
import rstr
from bank.models import Wallet
from banksite import settings
from rest_framework.test import APIRequestFactory


@pytest.fixture(scope='class')
def setup_and_teardown_db():
    start_command = 'docker compose -f tests/test_docker-compose.yml up -d'
    subprocess.run(['bash', '-c', start_command])
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test',
            'USER': 'test',
            'PASSWORD': 'test',
            'HOST': 'localhost',
            'PORT': '5434'}
    }
    yield
    stop_command = 'docker rm test -f -v'
    subprocess.run(['bash', '-c', stop_command])


@pytest.fixture
def create_user():

    def wrapper(body):
        username = body['username']
        password = make_password(body['password'])
        first_name = body['first_name']
        last_name = body['last_name']
        user_data = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
        user = User.objects.create(**user_data)
        user.save()
        return user

    return wrapper


@pytest.fixture
def get_token():
    endpoint = '/api/jwt/create'

    def wrapper(body):
        factory = APIRequestFactory()
        request = factory.post(endpoint, body, format='json')
        view = TokenObtainPairView.as_view()
        response = view(request)
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')
        return access_token, refresh_token

    return wrapper


@pytest.fixture
def create_wallet():

    def wrapper(user_id):
        wallet = Wallet.objects.create(user_id=user_id, wallet_id=rstr.xeger(r'[A-Z]{3}[-]\d{3}[-]\d{4}'))
        return wallet

    return wrapper
