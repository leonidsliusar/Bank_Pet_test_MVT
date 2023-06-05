from abc import ABC
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import ListWalletView, DetailWalletView
from bank.models import Wallet


@pytest.mark.usefixtures("setup_and_teardown_db", "db")
class BaseTest(ABC):
    username: str = 'test'
    password: str = 'test123!!'
    first_name: str = 'test'
    last_name: str = 'test'
    factory = APIRequestFactory()

    @property
    def get_payload(self):
        body = {
            "username": self.username,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
        return body


class TestTokenAPI(BaseTest):

    def test_reg_user_api(self):
        endpoint = '/api/users'
        body = self.get_payload
        request = self.factory.post(endpoint, body, format='json')
        view = UserViewSet.as_view({'post': 'create'})
        response = view(request)
        id = response.data['id']
        body.pop("password")
        expected_result = {'id': id, **body}
        user = User.objects.get(pk=id)
        assert response.status_code == 201
        assert response.data == expected_result
        assert user

    def test_get_tokens(self, create_user):
        body = self.get_payload
        user_wrapper = create_user
        user_wrapper(body)
        endpoint = '/api/jwt/create'
        body.pop("first_name")
        body.pop("last_name")
        request = self.factory.post(endpoint, body, format='json')
        view = TokenObtainPairView.as_view()
        response = view(request)
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')
        assert response.status_code == 200
        assert refresh_token
        assert access_token

    def test_refresh_refresh(self, create_user, get_token):
        body = self.get_payload
        user_wrapper = create_user
        user_wrapper(body)
        body.pop("first_name")
        body.pop("last_name")
        token_wrapper = get_token
        access_token, refresh_token = token_wrapper(body)
        endpoint = '/api/jwt/refresh'
        request = self.factory.post(endpoint, {"refresh": refresh_token}, format='json')
        view = TokenRefreshView.as_view()
        response = view(request)
        new_token = response.data.get('access')
        assert response.status_code == 200
        assert new_token
        assert new_token != access_token


class TestWalletAPI(BaseTest):

    def init_user(self, create_user, get_token, create_wallet=None) -> dict[str]:
        body = self.get_payload
        user_wrapper = create_user
        user = user_wrapper(body)
        self.user_id = user.id
        body.pop("first_name")
        body.pop("last_name")
        token_wrapper = get_token
        self.access_token, self.refresh_token = token_wrapper(body)
        if create_wallet:
            wallet_wrapper = create_wallet
            self.wallet = wallet_wrapper(self.user_id)
        transaction_body = {
            "source": 'test',
            "recipient": 'test',
            "quantity": '-100'
        }
        return transaction_body

    def test_get_list(self, create_user, get_token, create_wallet):
        self.init_user(create_user, get_token, create_wallet)
        endpoint = f'/api/v1/{self.user_id}/wallets'
        view = ListWalletView.as_view()
        request = self.factory.get(endpoint, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = view(request, self.user_id)
        assert response.status_code == 200

    def test_post_list(self, create_user, get_token):
        self.init_user(create_user, get_token)
        endpoint = f'/api/v1/{self.user_id}/wallets'
        view = ListWalletView.as_view()
        request = self.factory.post(endpoint, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = view(request, self.user_id)
        test_wallet = Wallet.objects.get(user_id=self.user_id)
        assert test_wallet
        assert response.status_code == 201

    def test_get_detail(self, create_user, get_token, create_wallet):
        self.init_user(create_user, get_token, create_wallet)
        endpoint = f'/api/v1/{self.user_id}/wallets/{self.wallet.wallet_id}'
        view = DetailWalletView.as_view()
        request = self.factory.get(endpoint, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = view(request, self.user_id, self.wallet.wallet_id)
        assert response.status_code == 200

    def test_delete_detail(self, create_user, get_token, create_wallet):
        self.init_user(create_user, get_token, create_wallet)
        endpoint = f'/api/v1/{self.user_id}/wallets/{self.wallet.wallet_id}'
        view = DetailWalletView.as_view()
        request = self.factory.delete(endpoint, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = view(request, self.user_id, self.wallet.wallet_id)
        wallet = Wallet.objects.filter(user_id=self.user_id)
        assert response.status_code == 200
        assert not wallet


class TestTransactionAPI(TestWalletAPI):

    def make_request_data(self, create_user, get_token, create_wallet):
        body = self.init_user(create_user, get_token, create_wallet)
        endpoint = f'http://testserver/api/v1/{self.user_id}/transaction'
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        return body, endpoint, client

    def test_post_transaction_source_doesnt_exists(self, create_user, get_token, create_wallet):
        body, endpoint, client = self.make_request_data(create_user, get_token, create_wallet)
        response = client.post(endpoint, body)
        assert response.status_code == 400
        assert response.data == {f'Source {body["source"]} wallet doesn\'t exists'}

    def test_post_transaction_target_doesnt_exists(self, create_user, get_token, create_wallet):
        body, endpoint, client = self.make_request_data(create_user, get_token, create_wallet)
        body["source"] = self.wallet.wallet_id
        response = client.post(endpoint, body)
        assert response.status_code == 400
        assert response.data == {f'Target {body["recipient"]} wallet doesn\'t exists'}

    def test_post_transaction_source_eq_target(self, create_user, get_token, create_wallet):
        body, endpoint, client = self.make_request_data(create_user, get_token, create_wallet)
        body["source"] = self.wallet.wallet_id
        body["recipient"] = body["source"]
        response = client.post(endpoint, body)
        assert response.status_code == 400
        assert response.data == {f'Source {body["source"]} wallet equal to target {body["recipient"]} wallet'}

    def test_post_transaction_invalid_amount(self, create_user, get_token, create_wallet):
        body, endpoint, client = self.make_request_data(create_user, get_token, create_wallet)
        wallet_wrapper = create_wallet
        target_wallet = wallet_wrapper(self.user_id)
        body["source"] = self.wallet.wallet_id
        body["recipient"] = target_wallet.wallet_id
        response = client.post(endpoint, body)
        assert response.status_code == 400
        assert response.data == {f'Invalid amount {body["quantity"]}'}

    def test_post_transaction_bad_balance(self, create_user, get_token, create_wallet):
        body, endpoint, client = self.make_request_data(create_user, get_token, create_wallet)
        wallet_wrapper = create_wallet
        target_wallet = wallet_wrapper(self.user_id)
        body["source"] = self.wallet.wallet_id
        body["recipient"] = target_wallet.wallet_id
        body["quantity"] = 100
        response = client.post(endpoint, body)
        assert response.status_code == 400
        assert response.data == {'Not enough money on source wallet'}

    def test_post_transaction_success(self, create_user, get_token, create_wallet):
        body, endpoint, client = self.make_request_data(create_user, get_token, create_wallet)
        wallet_wrapper = create_wallet
        target_wallet = wallet_wrapper(self.user_id)
        body["source"] = self.wallet.wallet_id
        body["recipient"] = target_wallet.wallet_id
        body["quantity"] = 100
        self.wallet.balance = 100
        self.wallet.save()
        response = client.post(endpoint, body)
        assert response.status_code == 200
        assert response.data == {'Transaction successful'}
