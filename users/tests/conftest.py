import pytest

from users.models import User


@pytest.fixture
def username(db):
    return "username"


@pytest.fixture
def user(db, username):
    return User.objects.create(username=username)
