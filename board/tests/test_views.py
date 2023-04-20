import pytest
from rest_framework.reverse import reverse

from board.models import Board, BoardMembership


@pytest.fixture
def board_creation_payload(board_name):
    return {"name": board_name}


def test_cannot_create_board_as_unauthorized_user(api_client, board_creation_payload):
    url = reverse("board:board-list")

    response = api_client.post(url, board_creation_payload)

    assert response.status_code == 403


def test_creates_board(authenticated_client, board_name, board_creation_payload, user):
    url = reverse("board:board-list")

    response = authenticated_client.post(url, board_creation_payload)

    assert response.status_code == 201
    assert Board.objects.filter(owner=user, name=board_name).exists()


def test_creates_board_membership(
    authenticated_client, board_name, board_creation_payload, user
):
    url = reverse("board:board-list")

    response = authenticated_client.post(url, board_creation_payload)

    assert BoardMembership.objects.filter(
        board__slug=response.data["slug"], user=user, role=BoardMembership.Role.ADMIN
    ).exists()
