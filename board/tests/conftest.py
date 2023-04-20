import pytest

from board.models import Board, BoardMembership
from users.tests.conftest import *


@pytest.fixture
def board_name():
    return "KnbnBoard"


@pytest.fixture
def board(db, user, board_name):
    board = Board.objects.create(name=board_name, owner=user)
    BoardMembership.objects.create(board=board, user=user)
    return board
