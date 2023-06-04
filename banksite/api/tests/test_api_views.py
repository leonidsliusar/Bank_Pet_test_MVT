import pytest
from rest_framework.test import APIRequestFactory
from djoser.views import UserViewSet

factory = APIRequestFactory()


@pytest.mark.usefixtures("setup_and_teardown_db", "django_db")
class TestAPI:


@pytest.mark.django_db
@pytest.mark.parametrize("username, password, first_name, last_name", [
    ('test', 'test123!!', 'test', 'test'),
])
def test_reg_user_api(setup_and_teardown_db, username, password, first_name, last_name):
    endpoint = 'api/users/'
    body = {
        "username": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name
    }
    request = factory.post(endpoint, body, format='json')
    view = UserViewSet.as_view({'post': 'create'})
    response = view(request)
    body.pop("password")
    expected_result = {'id': 1, **body}
    assert response.status_code == 201
    assert response.data == expected_result


@pytest.mark.parametrize("username, password, first_name, last_name", [
    ('test', 'test123!!', 'test', 'test'),
])
def test_get_token(setup_and_teardown_db, )