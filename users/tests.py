import pytest
from rest_framework.test import APIClient

from .models import User


@pytest.fixture
def api_client(db):
    return APIClient()


# ################################################################# #
# ####################### TEST registration ####################### #


def test_registration(db, api_client: APIClient):
    user_count = User.objects.count()
    response = api_client.post('/signup/',
                               {'username': 'User_4',
                                'first_name': 'Jean',
                                'last_name': 'Bart',
                                'email': 'jeanbart@test.fr',
                                'password': 'password999',
                                'password2': 'password999'})
    assert response.status_code == 201
    assert User.objects.count() == user_count + 1


# ################################################################# #
# #######################    TEST login     ####################### #

def test_login_authorized(db, api_client: APIClient):
    User.objects.create_user(username='User_4', password='password999')
    response = api_client.post('/login/',
                               {'username': 'User_4',
                                'password': 'password999',
                                })
    assert response.status_code == 200


def test_login_non_authorized(db, api_client: APIClient):
    User.objects.create_user(username='User_5', password='password999')
    response = api_client.post('/login/',
                               {'username': 'User_4',
                                'password': 'password999',
                                })
    assert response.status_code == 401
