import pytest

from board.models import Board
from users.tests.conftest import *


@pytest.fixture
def board_name():
    return "KnbnBoard"


@pytest.fixture
def board(db, user, board_name):
    return Board.objects.create(name=board_name, owner=user)
