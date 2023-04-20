import pytest

from users.models import User
from tests.conftest import *


@pytest.fixture
def username(db):
    return "username"


@pytest.fixture
def user(db, username):
    return User.objects.create(username=username)


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user)
    return api_client
