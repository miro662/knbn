from users.models import User


def test_no_users(db):
    assert User.objects.count() == 0
