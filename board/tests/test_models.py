import pytest
from django.db.utils import IntegrityError
from django.utils.text import slugify

from board.models import Board, BoardMembership


def test_creates_slug_on_save(user, board_name):
    slug = slugify(user.username + "-" + board_name)
    board = Board.objects.create(name=board_name, owner=user)

    assert board.slug == slug


@pytest.mark.skip("Bug in capturing integrity error")
def test_creating_two_memberships_for_a_single_user_causes_error(db, user, board):
    BoardMembership.objects.create(user=user, board=board)  # first membership

    with pytest.raises(IntegrityError):
        BoardMembership.objects.create(user=user, board=board)  # second membership
